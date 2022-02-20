import cv2
import random
import numpy as np
from models.basic_filter import basic_filter


class sharpen(basic_filter):
    def __init__(self, debug=False):
        super().__init__(debug)
        self.description = """Modifies the resolution and contrast around
                              edges for the appearance of a 'sharper' image"""
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
