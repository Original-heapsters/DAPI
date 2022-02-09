import cv2
import io
import os
import shutil
import uuid
from utils import (allowed_file,
                   clear_dir,
                   apply_random_filters)
from Filters import (circle,
                     laserEyes,
                     noise,
                     brightnessContrast,
                     bulge,
                     inpaint,
                     sharpen,
                     swirl)
from werkzeug.utils import secure_filename
from flask import (Flask,
                   jsonify,
                   request,
                   redirect,
                   url_for,
                   send_file,
                   render_template)

import redis
app = Flask(__name__)
app.config.from_pyfile('default.default_settings')


@app.before_first_request
def initialize():
    global redis_instance
    global filter_classes
    redis_url = os.environ.get('REDIS_URL') or app.config['REDIS_URL']
    redis_instance = redis.Redis.from_url(redis_url)
    eye_classifier = os.path.join('./Filters/resources',
                                  app.config['EYE_CLASSIFIER'])
    smile_classifier = os.path.join('./Filters/resources',
                                    app.config['SMILE_CLASSIFIER'])
    face_classifier = os.path.join('./Filters/resources',
                                   app.config['FACE_CLASSIFIER'])
    eye_cascade = cv2.CascadeClassifier(eye_classifier)
    smile_cascade = cv2.CascadeClassifier(smile_classifier)
    face_cascade = cv2.CascadeClassifier(face_classifier)
    filter_classes = {
        'circle': circle.circle(eye_cascade),
        'laserEyes': laserEyes.laserEyes(),
        'noise': noise.noise(),
        'brightness': brightnessContrast.brightnessContrast(),
        'bulge': bulge.bulge(),
        'inpaint': inpaint.inpaint(eye_cascade, smile_cascade, face_cascade),
        'sharpen': sharpen.sharpen(),
        'swirl': swirl.swirl(),
        }


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/420')
def swag():
    return "69 BROOOOOO!"


@app.route('/home')
def upload_form():
    return render_template('upload.html')


def process_image(filter_name=None):
    # Clear out static folder to preserve space
    clear_dir(app.config['UPLOAD_FOLDER'])

    # check if the post request has the file part
    if 'file' not in request.files:
        return 'No file was uploaded'

    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return 'No selected file'

    if file and allowed_file(file.filename):
        file_components = file.filename.rsplit('.', 1)
        name = uuid.uuid4().hex
        filename = secure_filename(name + '.' + file_components[-1])
        input_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_file)
        app.logger.debug(f'Saving temp file to {input_file}')

        if filter_name and filter_classes[filter_name]:
            chosen_filter = filter_classes[filter_name]
            filtered_img = apply_random_filters([chosen_filter], input_file)
        else:
            possible_filters = list(filter_classes.values())
            filtered_img = apply_random_filters(possible_filters, input_file)

        # Overwrite uploaded img with filtered version
        if filtered_img is not None:
            shutil.move(filtered_img, input_file)
        with open(input_file, 'rb') as f:
            file_bytes = f.read()
            redis_instance.setex(name, app.config['REDIS_TTL'], file_bytes)
            app.logger.debug(f'Saving filtered img bytes to redis key {name}')

        return filename, name
    return f'File not allowed {file.filename}'


@app.route('/home', methods=['POST'])
def upload_file():
    asApi = request.args.get('asApi')
    result = process_image()
    filename, name = result
    if asApi and name:
        # send file as attachment as api response
        return send_file(
            io.BytesIO(redis_instance.get(name)),
            as_attachment=True,
            attachment_filename=filename
        )
    elif not asApi and filename:
        # re-render to barebones frontend
        return render_template('upload.html', filename=filename)
    else:
        return result


@app.route('/filters/<filter_name>', methods=['POST'])
def isolate_filter(filter_name):
    result = process_image(filter_name)
    filename, name = result

    # send file as attachment as api response
    return send_file(
        io.BytesIO(redis_instance.get(name)),
        as_attachment=True,
        attachment_filename=filename
    )


@app.route('/filters/<filter_name>', methods=['GET'])
def get_filter_info(filter_name):
    # send file as attachment as api response
    return jsonify(filter_classes[filter_name].get_info())


@app.route('/filters', methods=['GET'])
def get_filter_names():
    return jsonify(list(filter_classes.keys()))


@app.route('/display/<filename>')
def display_image(filename):
    return redirect(
            url_for('static', filename='uploads/' + filename),
            code=301
            )


if __name__ == '__main__':
    app_port = os.environ.get('PORT') or app.config['PORT']
    app.logger.info(f'Launching at {app.config["HOST"]}:{app_port}')
    app.run(debug=app.config['DEBUG'],
            port=app_port,
            host=app.config['HOST'])
