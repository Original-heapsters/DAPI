import os
import tempfile
import cv2
import random
import numpy as np


class swirl(object):
    def __init__(self):
        dirname = os.path.dirname(__file__)
        self.resources = os.path.join(dirname, 'resources')
        self.additives = os.path.join(dirname, 'additives')

    def get_info(self):
        return {
                'name': __class__.__name__,
                'description': """Gets a rand center + swirl a rand amount""",
                'randomized_aspects': ['swirl center', 'swirl radius'],
                'performance_impact': 1,
                'requires_face': False,
                }

    def filter_image(self, input, coords=None):
        im = cv2.imread(input)

        # parameters controlling the transform
        cx = random.uniform(im.shape[1]/4, im.shape[1]/2)
        cy = random.uniform(im.shape[1]/4, im.shape[0]/2)
        # a, b and c are General Archimedean spiral parameters
        a = -1
        b = 2
        c = 1
        # select the region around (cx, cy) to apply the transform
        r = random.uniform(0.1, 0.5)

        x = np.linspace(0, im.shape[1], im.shape[1], dtype=np.float32)
        y = np.linspace(0, im.shape[0], im.shape[0], dtype=np.float32)
        xv, yv = np.meshgrid(x - cx, y - cy)

        mag, ang = cv2.cartToPolar(xv, yv)
        nmag = cv2.normalize(mag, None, norm_type=cv2.NORM_MINMAX)

        cartEq = (ang + (a + b*np.pi*nmag**(1.0/c))*(nmag < r))
        sxv, syv = cv2.polarToCart(mag, cartEq)
        return cv2.remap(im,
                         sxv + cx,
                         syv + cy,
                         cv2.INTER_LINEAR)

    def identify_prep(self, input):
        grayImage = cv2.cvtColor(input, cv2.COLOR_BGR2GRAY)
        return grayImage

    # Find eyes
    def identify_features(self, input):
        return None

    def apply_filter(self, input, debug=False):
        print('Applying filter')
        print(self.get_info())
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
    filterClass = swirl()
    filterClass.apply_filter(originalImg, debug=True)
