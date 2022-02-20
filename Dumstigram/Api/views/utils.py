import os
import shutil
import random
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


def clear_dir(folder_path):
    os.makedirs(folder_path, exist_ok=True)
    files = os.listdir(folder_path)
    if len(files) > 5:
        for file_object in files:
            file_path = os.path.join(folder_path, file_object)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            else:
                shutil.rmtree(file_path)


def apply_random_filters(filters, input_img):
    running_img = None
    num_filters = 1 if not isinstance(filters, list) else len(filters)
    if num_filters == 1:
        running_img = random.choice(filters).apply_filter(input_img)
    else:
        for k in range(random.randint(0, num_filters - 1)):
            img_src = running_img if running_img else input_img
            running_img = random.choice(filters).apply_filter(img_src)
    return running_img


def process_image(filter_name=None):
    # Clear out static folder to preserve space
    clear_dir(uploads)

    # check if the post request has the file part
    if 'file' not in request.files:
        return 'No file was uploaded'

    file = request.files['file']
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

        if filter_name and filter_classes[filter_name]:
            chosen_filter = filter_classes[filter_name]
            filtered_img = apply_random_filters([chosen_filter], input_file)
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

        return filename, name
    return f'File not allowed {file.filename}'
