import os
import tempfile
import cv2
import random
import numpy as np


class inpaint(object):
    def __init__(self, eye_cascade, smile_cascade, face_cascade):
        self.eye_cascade = eye_cascade
        self.smile_cascade = smile_cascade
        self.face_cascade = face_cascade
        self.detection_mode = 'eyes'
        self.laser_count = 5
        self.identifier = 'haar_eye_tree_glasses.xml'

    def get_info(self):
        return {
                'name': __class__.__name__,
                'description': """Uses inpaint to remove detected eyes""",
                'randomized_aspects': ['inpaint radius'],
                'performance_impact': 3,
                'requires_face': True,
                }

    def filter_image(self, input, coords=None):
        if coords is None or len(coords) == 0:
            return input

        mask = np.zeros(input.shape[:2], dtype='uint8')

        for pts in coords:
            cv2.rectangle(mask, pts, 255, -1)
        output = cv2.inpaint(input,
                             mask,
                             random.uniform(50, 100),
                             flags=random.choice([cv2.INPAINT_TELEA]))
        return output

    def identify_prep(self, input):
        grayImage = cv2.cvtColor(input, cv2.COLOR_BGR2GRAY)
        return grayImage

    # Find eyes
    def identify_features(self, input):
        prepped_img = self.identify_prep(input)
        if self.detection_mode == 'eyes':
            eyes = self.eye_cascade.detectMultiScale(prepped_img)
            return eyes
        elif self.detection_mode == 'smile':  # Experimental, does not work
            faces = self.face_cascade.detectMultiScale(prepped_img, 1.3, 5)
            smiles = []
            for (x, y, w, h) in faces:
                smiles.append(self.smile_cascade.detectMultiScale(prepped_img,
                                                                  1.8,
                                                                  20))
            return smiles

    def apply_filter(self, input, debug=False):
        original = cv2.imread(input)

        if debug:
            cv2.imshow('Original', original)
        coords = self.identify_features(original)
        filtered = self.filter_image(original, coords)

        if debug and filtered is not None:
            cv2.imshow('Filter Applied', filtered)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        tfile, tpath = tempfile.mkstemp(".png")
        cv2.imwrite(tpath, filtered)
        return tpath


if __name__ == '__main__':
    classifier = os.path.join('./resources',
                              'haar_eye_tree_glasses.xml')
    eye_cascade = cv2.CascadeClassifier(classifier)
    originalImg = '../uploads/test.png'
    filterClass = inpaint(eye_cascade)
    filterClass.apply_filter(originalImg, debug=True)
