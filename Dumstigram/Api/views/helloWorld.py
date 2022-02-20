from flask import Blueprint

helloWorld = Blueprint('helloWorld', __name__)


@helloWorld.route('/')
@helloWorld.route('/index')
@helloWorld.route('/hello')
@helloWorld.route('/test')
def index():
    return 'Hello World!'
