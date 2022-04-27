import io
import hashlib
from flask import Blueprint, current_app, request, send_file

with current_app.app_context():
    redis = current_app.config['REDIS']
    users = Blueprint('users', __name__)


@users.route('/login/fake', methods=['POST'])
def fake_login():
    username = request.form.get('username', None)
    avatar = request.files.get('avatar', None)
    hash_object = hashlib.sha256(str.encode(username))
    user_hash = hash_object.hexdigest()
    username_key = '{}:username:'.format(user_hash)
    avatar_key = '{}:avatar:'.format(user_hash)
    if not redis.get(username_key):
        print('new stuff')
        redis.setex(username_key, current_app.config['REDIS_TTL'], username)
        redis.setex(avatar_key, current_app.config['REDIS_TTL'], avatar.read())

    return send_file(
        io.BytesIO(redis.get(avatar_key)),
        as_attachment=True,
        attachment_filename=username + '.png'
    )
