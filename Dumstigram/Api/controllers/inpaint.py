import os
import cv2
import random
import numpy as np
if __name__ == '__main__':
    import sys
    sys.path.append('../models')
    from face_filter import face_filter
else:
    from models.face_filter import face_filter


class inpaint(face_filter):
    def __init__(self,
                 eye_cascade,
                 smile_cascade,
                 face_cascade,
                 mode,
                 debug=False):
        super().__init__(eye_cascade, smile_cascade, face_cascade, mode, debug)
        self.description = """Uses inpaint to remove detected eyes"""
        self.randomization = ['inpaint radius']

    def filter_image(self, input, coords=None):
        if coords is None or len(coords) == 0:
            return input

        mask = np.zeros(input.shape[:2], dtype='uint8')

        for pts in coords:
            adj_w = int(pts[2] / 2)
            adj_h = int(pts[3] / 2)
            adj_x = int(pts[0] + adj_w/2)
            adj_y = int(pts[1] + adj_h/2)
            # Reducing size of detected rectangle for performance reasons
            smaller_pts = [adj_x, adj_y, adj_w, adj_h]
            cv2.rectangle(mask, smaller_pts, 255, -1)
        output = cv2.inpaint(input,
                             mask,
                             random.uniform(50, 100),
                             flags=random.choice([cv2.INPAINT_TELEA]))
        return output


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
    filterClass = inpaint(eye_cascade,
                          smile_cascade,
                          face_cascade,
                          mode='smile',
                          debug=True)
    filterClass.apply_filter(originalImg)
