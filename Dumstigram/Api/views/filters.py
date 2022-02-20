import io
from flask import Blueprint, current_app, jsonify, send_file
from . import utils

with current_app.app_context():
    redis = current_app.config['REDIS']
    filter_classes = current_app.config['FILTER_CLASSES']
    filters = Blueprint('filters', __name__)


@filters.route('/<filter_name>', methods=['POST'])
def isolate_filter(filter_name):
    result = utils.process_image(filter_name)
    filename, name = result

    # send file as attachment as api response
    return send_file(
        io.BytesIO(redis.get(name)),
        as_attachment=True,
        attachment_filename=filename
    )


@filters.route('/<filter_name>', methods=['GET'])
def get_filter_info(filter_name):
    # send file as attachment as api response
    return jsonify(filter_classes[filter_name].get_info())


@filters.route('', methods=['GET'])
def get_filter_names():
    return jsonify(list(filter_classes.keys()))
