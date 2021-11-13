import os
import tempfile
import cv2
import random


class brightnessContrast(object):
    def __init__(self):
        dirname = os.path.dirname(__file__)

    def filter_image(self, input, coords=None):
        alpha = random.uniform(1.0, 3.0)  # Contrast control (1.0-3.0)
        beta = random.uniform(0, 100)  # Brightness control (0-100)

        adjusted = cv2.convertScaleAbs(input, alpha=alpha, beta=beta)
        return adjusted

    def identify_prep(self, input):
        return None

    # Find eyes
    def identify_features(self, input):
        return None

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
    filterClass = brightnessContrast()
    filterClass.apply_filter(originalImg, debug=True)
