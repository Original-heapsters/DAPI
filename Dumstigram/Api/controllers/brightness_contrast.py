import cv2
import random
if __name__ == '__main__':
    import sys
    sys.path.append('../models')
    from basic_filter import basic_filter
else:
    from models.basic_filter import basic_filter


class brightness_contrast(basic_filter):
    def __init__(self, debug=False):
        super().__init__(debug)
        self.friendly_name = 'Brightness & Contrast'
        self.description = """Adjusts brightness and contrast of image"""
        self.randomization = ['contrast amount', 'brightness amount']

    def filter_image(self, input):
        alpha = random.uniform(1.0, 3.0)  # Contrast control (1.0-3.0)
        beta = random.uniform(0, 100)  # Brightness control (0-100)

        adjusted = cv2.convertScaleAbs(input, alpha=alpha, beta=beta)
        return adjusted


if __name__ == '__main__':
    originalImg = '../uploads/test.png'
    filterClass = brightness_contrast(debug=True)
    filterClass.apply_filter(originalImg)
