import os
import json
import base64
from flask import Blueprint, current_app
from .utils import clear_dir

with current_app.app_context():
    redis = current_app.config['REDIS']
    recent = Blueprint('recent', __name__)
    recent_folder = current_app.config['RECENT_FOLDER']
    users_folder = current_app.config['USERS_FOLDER']


def save_avatar(full_url):
    avatar_file_name = full_url[0].rsplit('/')[-1]
    avatar_hash = avatar_file_name[:-4]
    avatar_key = '{}:avatar'.format(avatar_hash)
    print(avatar_key)

    dest_path = os.path.join(users_folder, avatar_file_name)
    with open(dest_path, 'wb') as f:
        avatar_bytes = redis.get(avatar_key)
        f.write(avatar_bytes)
        f.close()


@recent.route('<num_recent>', methods=['GET'])
def get_recent_frys(num_recent):
    clear_dir(recent_folder, 20)
    return_obj = {}
    recent_keys = redis.scan_iter('posts:*')
    for byte_key in recent_keys:
        r_key = byte_key.decode('utf-8')
        expiration = str(redis.ttl(r_key))
        dest_path = os.path.join(recent_folder, r_key + '.png')
        if not os.path.exists(recent_folder):
            os.makedirs(recent_folder)
        with open(dest_path, 'wb') as f:
            post_info = redis.get(r_key)
            full_post = json.loads(post_info.decode('ascii'))
            img_bytes = full_post.get('bytes', None)
            that = img_bytes.encode('ascii')
            bytess = base64.b64decode(that)
            f.write(bytess)
            f.close()
            full_avatar_url = full_post.get('avatar_url', None),
            save_avatar(full_avatar_url)
            return_obj[str(r_key)] = {
                'img_url': dest_path,
                'username': full_post.get('username', None),
                'avatar_url': full_post.get('avatar_url', None),
                'caption': full_post.get('caption', None),
                'expiration': expiration,
                'created': full_post.get('created', None),
                }

    return return_obj
