import os
import cv2
import random
if __name__ == '__main__':
    import sys
    sys.path.append('../models')
    from face_overlay_filter import face_overlay_filter
else:
    from models.face_overlay_filter import face_overlay_filter


class laser_eyes(face_overlay_filter):
    def __init__(self,
                 eye_cascade,
                 smile_cascade,
                 face_cascade,
                 mode,
                 debug=False):
        super().__init__(eye_cascade, smile_cascade, face_cascade, mode, debug)
        self.description = """Add random set of lasers on detected eyes"""
        self.randomization = ['laser chosen']
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        self.additives = os.path.join(curr_dir, 'lasers')

    def calc_position(self, x, y, overlay):
        x_offset = x
        y_offset = y + int(overlay.shape[0] / 2)
        y1, y2 = y_offset, y_offset + overlay.shape[0]
        x1, x2 = x_offset, x_offset + overlay.shape[1]
        return x1, y1, x2, y2

    def filter_image(self, input, coords=None):
        if coords is None:
            return input

        laser_chosen = random.choice(os.listdir(self.additives))
        overlay = cv2.imread(self.additives + '/' + laser_chosen, -1)

        for (x, y, w, h) in coords:
            adjustedX = x - int(w/2)
            adjustedY = y - int(h/2)
            adjustedW = w * 2
            resized = self.resize_overlay(adjustedW, overlay)
            x1, y1, x2, y2 = self.calc_position(adjustedX, adjustedY, resized)
            input = self.overlay_with_alpha(x1, y1, x2, y2, resized, input)
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
    originalImg = '../uploads/smileLady.jpg'
    filterClass = laser_eyes(eye_cascade,
                             smile_cascade,
                             face_cascade,
                             mode='eyes',
                             debug=True)
    filterClass.apply_filter(originalImg)
