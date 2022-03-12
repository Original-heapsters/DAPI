# import io
import base64
from flask import Blueprint, current_app
# from . import utils

with current_app.app_context():
    redis = current_app.config['REDIS']
    recent = Blueprint('recent', __name__)


@recent.route('<num_recent>', methods=['GET'])
def get_recent_frys(num_recent):
    print(num_recent)
    return_obj = {}
    keys_to_fetch = int(num_recent)
    recent_keys = redis.scan_iter('*', keys_to_fetch)
    for r_key in recent_keys:
        print(r_key)
        print(base64.b64encode(redis.get(r_key)))
        return_obj[str(r_key)] = str(base64.b64encode(redis.get(r_key)))
    return return_obj
