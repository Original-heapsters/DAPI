import os
import io
from flask import Flask, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
from Filters import laserEyes
import redis
app = Flask(__name__)
app.config.from_pyfile('default.default_settings')
app.config.from_envvar('DAPI_ENV_OVERRIDE', silent=True)
r = redis.Redis(host='localhost', port=6379, db=0)


ALLOWED_EXTENSIONS = {'PNG', 'png', 'jpg', 'jpeg'}


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/420')
def swag():
    return "69 BROOOOO!"


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
        print(dest_file)

        # choose random filter and apply it here
        filterClass = laserEyes.laserEyes()
        filtered_image = filterClass.apply_filter(dest_file)
        with open(filtered_image, 'rb') as f:
            s = f.read()
            r.setex('test', 1000, s)

        return send_file(
            io.BytesIO(r.get('test')),
            as_attachment=True,
            attachment_filename=filtered_image
        )

        return redirect(url_for('uploaded_file',
                                filename=filtered_image))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_file(filename)


if __name__ == '__main__':
    print(app.config['PORT'])
    app.run(debug=app.config['DEBUG'],
            port=app.config['PORT'],
            host=app.config['HOST'])
