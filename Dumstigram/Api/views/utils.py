import os
import io
import shutil
import random
import requests
import uuid
from flask import current_app, request
from werkzeug.utils import secure_filename

with current_app.app_context():
    redis = current_app.config['REDIS']
    filter_classes = current_app.config['FILTER_CLASSES']
    uploads = current_app.config['UPLOAD_FOLDER']
    logger = current_app.logger

ALLOWED_EXTENSIONS = {'PNG', 'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def clear_dir(folder_path, max_limit=5):
    os.makedirs(folder_path, exist_ok=True)
    files = os.listdir(folder_path)
    if len(files) > max_limit:
        for file_object in files:
            file_path = os.path.join(folder_path, file_object)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            else:
                shutil.rmtree(file_path)


def apply_random_filters(filters, input_img, sequential=False):
    running_img = None
    num_filters = 1 if not isinstance(filters, list) else len(filters)
    if num_filters == 1:
        running_img = random.choice(filters).apply_filter(input_img)
    elif sequential:
        for filter in filters:
            img_src = running_img if running_img else input_img
            running_img = filter.apply_filter(img_src)
    else:
        for k in range(random.randint(1, num_filters - 1)):
            img_src = running_img if running_img else input_img
            running_img = random.choice(filters).apply_filter(img_src)
    return running_img


def use_given_file(file, filter_names):
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return 'No selected file'

    if file and allowed_file(file.filename):
        file_components = file.filename.rsplit('.', 1)
        name = uuid.uuid4().hex
        filename = secure_filename(name + '.' + file_components[-1])
        input_file = os.path.join(uploads, filename)
        file.save(input_file)
        logger.debug(f'Saving temp file to {input_file}')
        return apply_filters(filter_names, input_file, filename, name)

    return f'File not allowed {file.filename}'


def use_file_url(file_url, filter_name):
    file_request = requests.get(file_url)

    name = uuid.uuid4().hex
    filename = secure_filename(name + '.png')
    input_file = os.path.join(uploads, filename)
    with open(input_file, "wb") as f:
        f.write(file_request.content)
        f.close()
    return apply_filters(filter_name, input_file, filename, name)


def check_items_in_list(input_dict, items):
    for item in items:
        if item not in input_dict:
            logger.error('{} was not found in {}'.format(item, input_dict))
            return False
    return True


def apply_filters(filter_names, input_file, filename, name):
    if filter_names and check_items_in_list(filter_classes, filter_names):
        seq_filters = [filter_classes[x] for x in filter_names]
        filtered_img = apply_random_filters(seq_filters,
                                            input_file,
                                            sequential=True)
    else:
        possible_filters = list(filter_classes.values())
        filtered_img = apply_random_filters(possible_filters, input_file)

    # Overwrite uploaded img with filtered version
    if filtered_img is not None:
        shutil.move(filtered_img, input_file)
    with open(input_file, 'rb') as f:
        file_bytes = f.read()
        redis.setex(name, current_app.config['REDIS_TTL'], file_bytes)
        logger.debug(f'Saving filtered img bytes to redis key {name}')

    return filename, name, input_file


def process_image(filter_name=None):
    # Clear out static folder to preserve space
    clear_dir(uploads)

    if 'file_url' in request.args:
        logger.debug('file_url is {}'.format(request.args))
        file_url = request.args.get('file_url')
        return use_file_url(file_url, filter_name)
    elif 'file' in request.files:
        logger.debug('file is {}'.format(request.files))
        file = request.files['file']
        return use_given_file(file, filter_name)
    else:
        logger.error('ERROR')
        return 'No file was uploaded or no url was provided'


def process_image_file(file, filter_names=None):
    # Clear out static folder to preserve space
    clear_dir(uploads)
    return use_given_file(file, filter_names)


def process_image_url(file_url, filter_names=None):
    # Clear out static folder to preserve space
    clear_dir(uploads)
    return use_file_url(file_url, filter_names)


def process_image_bytes(bytes, fileKey):
    # Clear out static folder to preserve space
    clear_dir(uploads)
    file_prefix = fileKey.split('posts:')[1] + '-' + uuid.uuid4().hex
    filename = file_prefix + '.png'
    input_file = os.path.join(uploads, filename)
    with open(input_file, "wb") as f:
        f.write(io.BytesIO(bytes).getbuffer())

    return apply_filters(None, input_file, filename, file_prefix)
