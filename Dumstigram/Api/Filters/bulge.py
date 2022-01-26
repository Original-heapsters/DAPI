import os
import tempfile
import cv2
import random
from wand.image import Image, PIXEL_INTERPOLATE_METHODS
import numpy as np
import math


class bulge(object):
    def __init__(self):
        dirname = os.path.dirname(__file__)
        self.resources = os.path.join(dirname, 'resources')
        self.additives = os.path.join(dirname, 'additives')
        self.laser_count = 5
        self.identifier = 'haar_eye_tree_glasses.xml'

    def get_info(self):
        return {
                'name': __class__.__name__,
                'description': """im/explodes the center of image""",
                'randomized_aspects': ['bulge amount'],
                'performance_impact': 2,
                'requires_face': False,
                }

    def filter_image(self, input, coords=None):
        def image_implode_method():
            with Image(filename=input) as img:
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
    filterClass = bulge()
    filterClass.apply_filter(originalImg, debug=True)
