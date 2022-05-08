import os
import cv2
import redis
from flask import (Flask)
from flask_cors import CORS
from flask_healthz import healthz
from controllers import (add_text,
                         arrow,
                         black_and_white,
                         brightness_contrast,
                         bulge,
                         celeb_eyes,
                         circle,
                         emoji_overlay,
                         grayscale,
                         inpaint,
                         laser_eyes,
                         mustache,
                         noise,
                         sharpen,
                         swirl)


def initialize():
    app.config.from_pyfile('default.default_settings')
    redis_url = os.environ.get('REDIS_URL') or app.config['REDIS_URL']
    redis_instance = redis.Redis.from_url(redis_url)
    app.config['REDIS'] = redis_instance
    eye_classifier = os.path.join('./controllers/resources',
                                  app.config['EYE_CLASSIFIER'])
    smile_classifier = os.path.join('./controllers/resources',
                                    app.config['SMILE_CLASSIFIER'])
    face_classifier = os.path.join('./controllers/resources',
                                   app.config['FACE_CLASSIFIER'])
    eye_cascade = cv2.CascadeClassifier(eye_classifier)
    smile_cascade = cv2.CascadeClassifier(smile_classifier)
    face_cascade = cv2.CascadeClassifier(face_classifier)
    filter_classes = {
        'add_text_top': add_text.add_text(is_top_text=True),
        'add_text_bottom': add_text.add_text(is_top_text=False),
        'arrow_eyes': arrow.arrow(eye_cascade,
                                  smile_cascade,
                                  face_cascade,
                                  'eyes'),
        'arrow_face': arrow.arrow(eye_cascade,
                                  smile_cascade,
                                  face_cascade,
                                  'face'),
        'black_and_white': black_and_white.black_and_white(),
        'brightness_contrast': brightness_contrast.brightness_contrast(),
        'bulge': bulge.bulge(),
        'celeb_eyes': celeb_eyes.celeb_eyes(eye_cascade,
                                            smile_cascade,
                                            face_cascade,
                                            'eyes'),
        'circle_eyes': circle.circle(eye_cascade,
                                     smile_cascade,
                                     face_cascade,
                                     'eyes'),
        'circle_smile': circle.circle(eye_cascade,
                                      smile_cascade,
                                      face_cascade,
                                      'smile'),
        'emoji_overlay': emoji_overlay.emoji_overlay(),
        'grayscale': grayscale.grayscale(),
        'inpaint_eyes': inpaint.inpaint(eye_cascade,
                                        smile_cascade,
                                        face_cascade,
                                        'eyes'),
        'laser_eyes': laser_eyes.laser_eyes(eye_cascade,
                                            smile_cascade,
                                            face_cascade,
                                            'eyes'),
        'mustache': mustache.mustache(eye_cascade,
                                      smile_cascade,
                                      face_cascade,
                                      'smile'),
        'noise': noise.noise(),
        'sharpen': sharpen.sharpen(),
        'swirl': swirl.swirl()
        }
    app.config['FILTER_CLASSES'] = filter_classes


app = Flask(__name__)
CORS(app)
with app.app_context():
    initialize()
    from views import (healthCheck,
                       display,
                       filters,
                       helloWorld,
                       home,
                       recent,
                       posts,
                       users
                       )
    app.config['HEALTHZ'] = {
        "live": healthCheck.liveness,
        "ready": healthCheck.readiness,
    }
    app.register_blueprint(healthz, url_prefix="/healthz")
    app.register_blueprint(display.display, url_prefix='/display')
    app.register_blueprint(filters.filters, url_prefix='/filters')
    app.register_blueprint(helloWorld.helloWorld)
    app.register_blueprint(home.home, url_prefix='/home')
    app.register_blueprint(recent.recent, url_prefix='/recent')
    app.register_blueprint(posts.posts, url_prefix='/posts')
    app.register_blueprint(users.users, url_prefix='/users')

if __name__ == '__main__':
    app_port = os.environ.get('PORT') or app.config['PORT']
    app.logger.info(f'Bump Launching at url {app.config["HOST"]}:{app_port}')
    app.run(debug=app.config['DEBUG'],
            port=app_port,
            host=app.config['HOST'])
