import cv2
import math
import random
import numpy as np
from wand.image import Image, PIXEL_INTERPOLATE_METHODS
from models.basic_filter import basic_filter


class bulge(basic_filter):
    def __init__(self, debug=False):
        super().__init__(debug)
        self.description = """im/explodes the center of image"""
        self.randomization = ['bulge amount']
        self.performance_impact = 2

    def filter_image(self, input):
        def image_implode_method():
            with Image(filename=self.source_filename) as img:
                img.virtual_pixel = 'black'
                img.implode(random.uniform(1, -1),
                            random.choice(PIXEL_INTERPOLATE_METHODS))
                img_explode_opencv = np.array(img)
                img_explode_opencv = cv2.cvtColor(img_explode_opencv,
                                                  cv2.COLOR_RGB2BGR)
                return img_explode_opencv

        def remap_method():
            original = cv2.imread(input)
            # grab the dimensions of the image
            (h, w, _) = original.shape

            # set up the x and y maps as float32
            flex_x = np.zeros((h, w), np.float32)
            flex_y = np.zeros((h, w), np.float32)

            # create map with the barrel pincushion distortion formula
            scale_y = random.uniform(1, 5)
            scale_x = random.uniform(1, 5)
            center_x = random.uniform(0, w)
            center_y = random.uniform(0, h)
            radius = random.uniform(50, 200)
            amount = random.uniform(-20, 20)
            for y in range(h):
                delta_y = scale_y * (y - center_y)
                for x in range(w):
                    # determine if pixel is within an ellipse
                    delta_x = scale_x * (x - center_x)
                    distance = delta_x * delta_x + delta_y * delta_y
                    if distance >= (radius * radius):
                        flex_x[y, x] = x
                        flex_y[y, x] = y
                    else:
                        factor = 1.0
                        if distance > 0.0:
                            sin = math.sin(math.pi * math.sqrt(distance)
                                           / radius / 2)
                            factor = math.pow(sin, -amount)
                        flex_x[y, x] = factor * delta_x / scale_x + center_x
                        flex_y[y, x] = factor * delta_y / scale_y + center_y

            # do the remap  this is where the magic happens
            return cv2.remap(original, flex_x, flex_y, cv2.INTER_LINEAR)

        return random.choice([image_implode_method])()


if __name__ == '__main__':
    originalImg = '../uploads/test.png'
    filterClass = bulge(debug=True)
    filterClass.apply_filter(originalImg)
