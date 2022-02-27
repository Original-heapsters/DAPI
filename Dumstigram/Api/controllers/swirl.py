import cv2
import random
import numpy as np
if __name__ == '__main__':
    import sys
    sys.path.append('../models')
    from basic_filter import basic_filter
else:
    from models.basic_filter import basic_filter


class swirl(basic_filter):
    def __init__(self, debug=False):
        super().__init__(debug)
        self.description = """Gets a rand center + swirl a rand amount"""
        self.randomization = ['swirl center', 'swirl radius']

    def filter_image(self, input):
        # parameters controlling the transform
        cx = random.uniform(input.shape[1]/4, input.shape[1]/2)
        cy = random.uniform(input.shape[1]/4, input.shape[0]/2)
        # a, b and c are General Archimedean spiral parameters
        a = -1
        b = 2
        c = 1
        # select the region around (cx, cy) to apply the transform
        r = random.uniform(0.1, 0.5)

        x = np.linspace(0, input.shape[1], input.shape[1], dtype=np.float32)
        y = np.linspace(0, input.shape[0], input.shape[0], dtype=np.float32)
        xv, yv = np.meshgrid(x - cx, y - cy)

        mag, ang = cv2.cartToPolar(xv, yv)
        nmag = cv2.normalize(mag, None, norm_type=cv2.NORM_MINMAX)

        cartEq = (ang + (a + b*np.pi*nmag**(1.0/c))*(nmag < r))
        sxv, syv = cv2.polarToCart(mag, cartEq)
        return cv2.remap(input,
                         sxv + cx,
                         syv + cy,
                         cv2.INTER_LINEAR)


if __name__ == '__main__':
    originalImg = '../uploads/test.png'
    filterClass = swirl(debug=True)
    filterClass.apply_filter(originalImg)
