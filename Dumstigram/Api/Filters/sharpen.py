import tempfile
import cv2
import numpy as np


class sharpen(object):

    def filter_image(self, input, coords=None):
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        adjusted = cv2.filter2D(input, -1, kernel)

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
    filterClass = sharpen()
    filterClass.apply_filter(originalImg, debug=True)
