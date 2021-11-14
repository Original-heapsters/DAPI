import os
import tempfile
import cv2
from wand.image import Image
import numpy as np


class bulge(object):
    def __init__(self):
        dirname = os.path.dirname(__file__)
        self.resources = os.path.join(dirname, 'resources')
        self.additives = os.path.join(dirname, 'additives')
        self.laser_count = 5
        self.identifier = 'haar_eye_tree_glasses.xml'

    def filter_image(self, input, coords=None):
        with Image(filename=input) as img:
            img.virtual_pixel = 'black'
            img.implode(-0.5)
            img_explode_opencv = np.array(img)
            img_explode_opencv = cv2.cvtColor(img_explode_opencv,
                                              cv2.COLOR_RGB2BGR)
            return img_explode_opencv

    def identify_prep(self, input):
        grayImage = cv2.cvtColor(input, cv2.COLOR_BGR2GRAY)
        return grayImage

    # Find eyes
    def identify_features(self, input):
        prepped_img = self.identify_prep(input)
        classifier = os.path.join(self.resources, self.identifier)
        eye_cascade = cv2.CascadeClassifier(classifier)
        eyes = eye_cascade.detectMultiScale(prepped_img)
        return eyes

    def apply_filter(self, input, debug=False):
        original = cv2.imread(input)

        if debug:
            cv2.imshow('Original', original)
        coords = self.identify_features(original)
        filtered = self.filter_image(input, coords)

        if debug and filtered is not None:
            cv2.imshow('Filter Applied', filtered)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        tfile, tpath = tempfile.mkstemp(".png")
        cv2.imwrite(tpath, filtered)
        return tpath


if __name__ == '__main__':
    originalImg = '../uploads/test.png'
    filterClass = bulge()
    filterClass.apply_filter(originalImg, debug=True)
