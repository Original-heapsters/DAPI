import os
import cv2
import random
if __name__ == '__main__':
    import sys
    sys.path.append('../models')
    from face_filter import face_filter
else:
    from models.face_filter import face_filter


class circle(face_filter):
    def __init__(self,
                 eye_cascade,
                 smile_cascade,
                 face_cascade,
                 mode,
                 debug=False):
        super().__init__(eye_cascade, smile_cascade, face_cascade, mode, debug)
        self.description = """Places red cirle around eyes"""

    def filter_image(self, input, coords=None):
        if coords is None or len(coords) == 0:
            return input

        for pts in coords:
            rect_center = (pts[0] + int(pts[2]/2), pts[1] + int(pts[3]/2))
            red = (0, 0, 255)
            if random.randint(0, 1) == 0:
                # 50/50 chance to draw a cirlce for every detected eye
                cv2.circle(input,
                           rect_center,
                           random.randint(1, pts[3]),
                           red,
                           random.randint(2, 5))
        return input


if __name__ == '__main__':
    eye_classifier = os.path.join('./resources',
                                  'haar_eye_tree_glasses.xml')
    eye_cascade = cv2.CascadeClassifier(eye_classifier)
    face_classifier = os.path.join('./resources',
                                   'haarcascade_frontalface_default.xml')
    face_cascade = cv2.CascadeClassifier(face_classifier)
    smile_classifier = os.path.join('./resources',
                                    'haarcascade_smile.xml')
    smile_cascade = cv2.CascadeClassifier(smile_classifier)
    originalImg = '../uploads/test.png'
    filterClass = circle(eye_cascade,
                         smile_cascade,
                         face_cascade,
                         mode='eyes',
                         debug=True)
    filterClass.apply_filter(originalImg)
