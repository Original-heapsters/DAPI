from flask import Flask, request
app = Flask(__name__)
app.config.from_pyfile('default.default_settings')
app.config.from_envvar('DAPI_ENV_OVERRIDE', silent=True)


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/420')
def swag():
    return "69 BROOOOO!"


@app.route('/track', methods=['POST'])
def track():
    return {'tracking': request.get_json()}


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'],
            port=app.config['PORT'],
            host=app.config['HOST'])
