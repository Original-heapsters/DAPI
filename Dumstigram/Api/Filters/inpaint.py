import os
import tempfile
import cv2
import random
import numpy as np


class inpaint(object):
    def __init__(self):
        dirname = os.path.dirname(__file__)
        self.resources = os.path.join(dirname, 'resources')
        self.additives = os.path.join(dirname, 'additives')
        self.laser_count = 5
        self.identifier = 'haar_eye_tree_glasses.xml'


    def filter_image(self, input, coords=None):
        if coords is None:
            return None

        mask = np.zeros(input.shape[:2], dtype='uint8')

        for pts in coords:
            cv2.rectangle(mask, pts, 255, -1)
        output = cv2.inpaint(input, mask, random.uniform(50, 100), flags=random.choice([cv2.INPAINT_TELEA, cv2.INPAINT_NS]))
        return output

    def identify_prep(self, input):
        grayImage = cv2.cvtColor(input, cv2.COLOR_BGR2GRAY)
        return grayImage

    # Find eyes
    def identify_features(self, input):
        prepped_img = self.identify_prep(input)
        eye_cascade = cv2.CascadeClassifier(self.resources + '/' + self.identifier)
        eyes = eye_cascade.detectMultiScale(prepped_img)
        return eyes

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
    originalImg = '../uploads/test.png'
    filterClass = inpaint()
    filterClass.apply_filter(originalImg, debug=True)
