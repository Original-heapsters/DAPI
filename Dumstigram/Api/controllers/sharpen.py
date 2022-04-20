import cv2
import random
import numpy as np
if __name__ == '__main__':
    import sys
    sys.path.append('../models')
    from basic_filter import basic_filter
else:
    from models.basic_filter import basic_filter


class sharpen(basic_filter):
    def __init__(self, debug=False):
        super().__init__(debug)
        self.friendly_name = 'Sharpen'
        self.description = """Modifies the resolution and contrast around
                              edges for the appearance of a 'sharper' image"""
        self.example_url = 'https://pe-images.s3.amazonaws.com/photo-editing/cc/sharpen-unsharp-mask/unsharp-mask-radius-comparison.jpg'
        self.randomization = ['kernel']

    def filter_image(self, input):
        kernel = np.array([[-1, -1, -1],
                           [-1, random.uniform(8, 13), -1],
                           [-1, -1, -1]])
        adjusted = cv2.filter2D(input, -1, kernel)

        return adjusted


if __name__ == '__main__':
    originalImg = '../uploads/test.png'
    filterClass = sharpen(debug=True)
    filterClass.apply_filter(originalImg)
