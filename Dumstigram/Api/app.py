import io
import os
import shutil
import uuid
from utils import (allowed_file,
                   clear_dir,
                   apply_random_filters)
from Filters import (laserEyes,
                     noise,
                     brightnessContrast,
                     bulge,
                     inpaint,
                     sharpen)
from werkzeug.utils import secure_filename
from flask import (Flask,
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
    filter_classes = [
        laserEyes.laserEyes(),
        noise.noise(),
        brightnessContrast.brightnessContrast(),
        bulge.bulge(),
        inpaint.inpaint(),
        sharpen.sharpen(),
        ]


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/420')
def swag():
    return "69 BROOOOO!"


@app.route('/home')
def upload_form():
    return render_template('upload.html')


def process_image():
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
        dest_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(dest_file)
        app.logger.debug(f'Saving temp file to {dest_file}')

        filtered_img = apply_random_filters(filter_classes, dest_file)

        # Replace uploaded img with filtered version
        shutil.move(filtered_img, dest_file)
        with open(dest_file, 'rb') as f:
            file_bytes = f.read()
            redis_instance.setex(name, app.config['REDIS_TTL'], file_bytes)
            app.logger.debug(f'Saving filtered img bytes to redis key {name}')

        return filename, name
    return f'File not allowed {file.filename}'


@app.route('/home', methods=['POST'])
def upload_file_testing():
    result = process_image()
    filename, _ = result
    if filename:
        return render_template('upload.html', filename=filename)
    else:
        return result


@app.route('/upload', methods=['POST'])
def upload_file():
    result = process_image()
    filename, name = result
    if name:
        return send_file(
            io.BytesIO(redis_instance.get(name)),
            as_attachment=True,
            attachment_filename=filename
        )
    else:
        return result


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
