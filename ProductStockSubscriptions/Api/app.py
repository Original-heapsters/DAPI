from flask import Flask, request
app = Flask(__name__)


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
    app.run(debug=True, port='5000', host='0.0.0.0')
