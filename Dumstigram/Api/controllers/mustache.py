import os
import cv2
import random
if __name__ == '__main__':
    import sys
    sys.path.append('../models')
    from face_overlay_filter import face_overlay_filter
else:
    from models.face_overlay_filter import face_overlay_filter


class mustache(face_overlay_filter):
    def __init__(self,
                 eye_cascade,
                 smile_cascade,
                 face_cascade,
                 mode,
                 debug=False):
        super().__init__(eye_cascade, smile_cascade, face_cascade, mode, debug)
        self.friendly_name = 'Mustache'
        self.description = """Add random mustache on detected smiles"""
        self.example_url = 'https://funny-photo.s3.amazonaws.com/templates/1189/preview220.jpg'
        self.randomization = ['mustache chosen']
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        self.additives = os.path.join(curr_dir, 'mustaches')

    def calc_position(self, x, y, overlay):
        x_offset = x
        y_offset = y - int(overlay.shape[0] / 4)
        y1, y2 = y_offset, y_offset + overlay.shape[0]
        x1, x2 = x_offset, x_offset + overlay.shape[1]
        return x1, y1, x2, y2

    def filter_image(self, input, coords=None):
        if coords is None:
            return input

        mustache_chosen = random.choice(os.listdir(self.additives))
        overlay = cv2.imread(self.additives + '/' + mustache_chosen, -1)

        for (x, y, w, h) in coords:
            resized = self.resize_overlay(w, overlay)
            x1, y1, x2, y2 = self.calc_position(x, y, resized)
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
    filterClass = mustache(eye_cascade,
                           smile_cascade,
                           face_cascade,
                           mode='smile',
                           debug=True)
    filterClass.apply_filter(originalImg)
