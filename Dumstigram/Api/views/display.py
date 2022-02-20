from flask import Blueprint, redirect, url_for

display = Blueprint('display', __name__)


@display.route('/display/<filename>')
def display_image(filename):
    return redirect(
            url_for('static', filename='uploads/' + filename),
            code=301
            )
