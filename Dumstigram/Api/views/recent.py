import os
from flask import Blueprint, current_app
from .utils import clear_dir

with current_app.app_context():
    redis = current_app.config['REDIS']
    recent = Blueprint('recent', __name__)
    recent_folder = current_app.config['RECENT_FOLDER']


@recent.route('<num_recent>', methods=['GET'])
def get_recent_frys(num_recent):
    clear_dir(recent_folder, 20)
    return_obj = {}
    # keys_to_fetch = int(num_recent)
    recent_keys = redis.scan_iter('*')
    for byte_key in recent_keys:
        r_key = byte_key.decode('utf-8')
        expiration = str(redis.ttl(r_key))
        dest_path = os.path.join(recent_folder, r_key + '.png')
        if not os.path.exists(recent_folder):
            os.makedirs(recent_folder)
        with open(dest_path, 'wb') as f:
            f.write(redis.get(r_key))
            f.close()

        return_obj[expiration + '-' + str(r_key)] = dest_path
    return return_obj
