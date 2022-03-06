from flask import current_app
from flask_healthz import HealthError

with current_app.app_context():
    redis = current_app.config['REDIS']


def liveness():
    if not redis.ping():
        raise HealthError("Can't connect to the redis instance")


def readiness():
    print('test ready')
    with current_app.app_context():
        redis = current_app.config['REDIS']
    if not redis.ping():
        raise HealthError("Can't connect to the redis instance")
