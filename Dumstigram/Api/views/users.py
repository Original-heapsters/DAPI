import os
import hashlib
from flask import Blueprint, current_app, request
from .utils import clear_dir

with current_app.app_context():
    redis = current_app.config['REDIS']
    users = Blueprint('users', __name__)
    users_folder = current_app.config['USERS_FOLDER']


@users.route('/login/fake', methods=['POST'])
def fake_login():
    clear_dir(users_folder, 20)
    username = request.form.get('username', None)
    avatar = request.files.get('file', None)
    hash_object = hashlib.sha256(str.encode(username))
    user_hash = hash_object.hexdigest()
    username_key = '{}:username:'.format(user_hash)
    avatar_key = '{}:avatar'.format(user_hash)
    if not redis.get(username_key):
        redis.setex(username_key, current_app.config['REDIS_TTL'], username)
        redis.setex(avatar_key, current_app.config['REDIS_TTL'], avatar.read())

    dest_path = os.path.join(users_folder, user_hash + '.png')
    if not os.path.exists(users_folder):
        os.makedirs(users_folder)

    with open(dest_path, 'wb') as f:
        avatar_bytes = redis.get(avatar_key)
        f.write(avatar_bytes)
        f.close()

    return {
        'avatar_url': dest_path
    }
