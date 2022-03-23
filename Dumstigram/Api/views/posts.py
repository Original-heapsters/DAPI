import io
import base64
import json
from flask import Blueprint, current_app, render_template, request, send_file
from . import utils

with current_app.app_context():
    redis = current_app.config['REDIS']
    default_ttl = current_app.config['REDIS_TTL']
    posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route('', methods=['POST'])
@posts.route('/new', methods=['POST'])
@posts.route('/create', methods=['POST'])
def create_post():
    post_info = request.form
    file_input = request.files.get('file', None)

    if not post_info:
        raise ValueError("Missing post info")

    ttl = post_info.get('ttl', default_ttl)
    username = post_info.get('username', None)
    avatar = post_info.get('avatar', None)
    file_url = post_info.get('file_url', None)
    caption = post_info.get('caption', None)

    if file_url is not None:
        result = utils.process_image_url(file_url)
    elif file_input is not None:
        result = utils.process_image_file(file_input)
    else:
        raise ValueError("Missing both file and file url")

    filename, name, final_file = result
    # TODO FRY an entire profile
    # TODO deep fry the internet

    with open(final_file, 'rb') as f:
        file_bytes = f.read()
        post_obj = {
                    'bytes': base64.b64encode(file_bytes).decode('ascii'),
                    'username': username,
                    'avatar_url': avatar,
                    'caption': caption
                    }
        redis.setex('posts:{}'.format(name),
                    ttl,
                    json.dumps(post_obj).encode('utf-8'))

    # send file as attachment as api response
    return send_file(
        io.BytesIO(redis.get(name)),
        as_attachment=True,
        attachment_filename=filename
    )


@posts.route('/<post_id>')
def post_details(id):
    return render_template('upload.html')


@posts.route('/user/<user_id>')
def users_posts(id):
    return render_template('upload.html')


@posts.route('')
def upload_form():
    return render_template('upload.html')


@posts.route('', methods=['POST'])
def upload_file():
    asApi = request.args.get('asApi')
    print('asApi is {}'.format(asApi))
    result = utils.process_image()
    filename, name = result
    if asApi and name:
        # send file as attachment as api response
        return send_file(
            io.BytesIO(redis.get(name)),
            as_attachment=True,
            attachment_filename=filename
        )
    elif not asApi and filename:
        # re-render to barebones frontend
        return render_template('upload.html', filename=filename)
    else:
        return result
