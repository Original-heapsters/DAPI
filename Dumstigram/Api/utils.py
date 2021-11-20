import os
import shutil
import random
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
        for k in range(random.randint(1, num_filters - 1)):
            if not running_img:
                running_img = random.choice(filters).apply_filter(input_img)
            else:
                running_img = random.choice(filters).apply_filter(running_img)
    return running_img
