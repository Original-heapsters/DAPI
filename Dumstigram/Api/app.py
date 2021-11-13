import os
import io
import random
import uuid
import shutil
from flask import Flask, request, redirect, url_for, send_file, render_template
from werkzeug.utils import secure_filename
from Filters import laserEyes, noise, brightnessContrast, bulge, inpaint, sharpen
import redis
app = Flask(__name__)
app.config.from_pyfile('default.default_settings')
redis_url = os.environ.get('REDIS_URL') or app.config['REDIS_URL']
r = redis.Redis.from_url(redis_url)


ALLOWED_EXTENSIONS = {'PNG', 'png', 'jpg', 'jpeg'}


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/420')
def swag():
    return "69 BROOOOO!"


@app.route('/home')
def upload_form():
	return render_template('upload.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def upload_file():
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
        name = str(hash(file_components[0]))
        filename = secure_filename(name + '.' + file_components[-1])
        dest_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(dest_file)
        app.logger.debug(f'Saving temp file to {dest_file}')

        # choose random filter and apply it here
        filter_classes = [laserEyes.laserEyes(), noise.noise(), brightnessContrast.brightnessContrast(), bulge.bulge(), inpaint.inpaint()]
        filterClass = random.choice(filter_classes)
        filtered_image = filterClass.apply_filter(dest_file)
        with open(filtered_image, 'rb') as f:
            s = f.read()
            r.setex('test', 30, s)
            app.logger.debug('Saving temp file to redis key test')
            os.remove(dest_file)

        return send_file(
            io.BytesIO(r.get('test')),
            as_attachment=True,
            attachment_filename=filtered_image
        )


@app.route('/home', methods=['POST'])
def upload_file_testing():
    # Clear out static folder to preserve space
    shutil.rmtree(app.config['UPLOAD_FOLDER'])
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

        # choose random filter and apply it here
        filter_classes = [laserEyes.laserEyes(), noise.noise(), brightnessContrast.brightnessContrast(), bulge.bulge(), inpaint.inpaint()]
        filterClass = random.choice(filter_classes)
        filtered_image = filterClass.apply_filter(dest_file)

        shutil.move(filtered_image, dest_file)
        with open(dest_file, 'rb') as f:
            s = f.read()
            r.setex('test', 30, s)
            app.logger.debug('Saving temp file to redis key test')

        return render_template('upload.html', filename=filename)


@app.route('/display/<filename>')
def display_image(filename):
    print(filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_file(filename)


if __name__ == '__main__':
    app_port = os.environ.get('PORT') or app.config['PORT']
    app.logger.info(f'Launching at {app.config["HOST"]}:{app_port}')
    app.run(debug=app.config['DEBUG'],
            port=app_port,
            host=app.config['HOST'])
