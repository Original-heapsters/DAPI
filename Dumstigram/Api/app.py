from flask import Flask, request
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.config.from_pyfile('default.default_settings')
app.config.from_envvar('DAPI_ENV_OVERRIDE', silent=True)


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
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('uploaded_file',
                                    filename=filename))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'],
            port=app.config['PORT'],
            host=app.config['HOST'])
