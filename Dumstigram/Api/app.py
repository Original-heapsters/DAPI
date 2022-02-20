import os
import cv2
import redis
from flask import (Flask)
from controllers import (black_and_white,
                         grayscale,
                         brightness_contrast,
                         noise,
                         sharpen,
                         swirl)
from Filters import (arrow,
                     circle,
                     emojiOverlay,
                     laserEyes,
                     bulge,
                     inpaint)


def initialize():
    app.config.from_pyfile('default.default_settings')
    redis_url = os.environ.get('REDIS_URL') or app.config['REDIS_URL']
    redis_instance = redis.Redis.from_url(redis_url)
    app.config['REDIS'] = redis_instance
    eye_classifier = os.path.join('./Filters/resources',
                                  app.config['EYE_CLASSIFIER'])
    smile_classifier = os.path.join('./Filters/resources',
                                    app.config['SMILE_CLASSIFIER'])
    face_classifier = os.path.join('./Filters/resources',
                                   app.config['FACE_CLASSIFIER'])
    eye_cascade = cv2.CascadeClassifier(eye_classifier)
    smile_cascade = cv2.CascadeClassifier(smile_classifier)
    face_cascade = cv2.CascadeClassifier(face_classifier)
    filter_classes = {
        'arrow': arrow.arrow(eye_cascade),
        'circle': circle.circle(eye_cascade),
        'emojiOverlay': emojiOverlay.emojiOverlay(),
        'laserEyes': laserEyes.laserEyes(),
        'noise': noise.noise(),
        'grayscale': grayscale.grayscale(),
        'brightness': brightness_contrast.brightness_contrast(),
        'bulge': bulge.bulge(),
        'inpaint': inpaint.inpaint(eye_cascade, smile_cascade, face_cascade),
        'sharpen': sharpen.sharpen(),
        'swirl': swirl.swirl(),
        'black_and_white': black_and_white.black_and_white()
        }
    app.config['FILTER_CLASSES'] = filter_classes


app = Flask(__name__)
with app.app_context():
    initialize()
    from views import display, filters, helloWorld, home
    app.register_blueprint(display.display, url_prefix='/display')
    app.register_blueprint(filters.filters, url_prefix='/filters')
    app.register_blueprint(helloWorld.helloWorld)
    app.register_blueprint(home.home, url_prefix='/home')


if __name__ == '__main__':
    app_port = os.environ.get('PORT') or app.config['PORT']
    app.logger.info(f'Launching at {app.config["HOST"]}:{app_port}')
    app.run(debug=app.config['DEBUG'],
            port=app_port,
            host=app.config['HOST'])
