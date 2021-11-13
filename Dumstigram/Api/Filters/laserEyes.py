import os
import tempfile
import cv2
import random


class laserEyes(object):
    def __init__(self):
        dirname = os.path.dirname(__file__)
        self.resources = os.path.join(dirname, 'resources')
        self.additives = os.path.join(dirname, 'additives')
        self.laser_count = 5
        self.identifier = 'haar_eye_tree_glasses.xml'


    def filter_image(self, input, coords=None):
        if coords is None:
            return None

        laser_chosen = 'laser_' + str(random.randint(1,self.laser_count))
        overlay = cv2.imread(self.additives + '/' + laser_chosen + '.png', -1)

        def resize_overlay(dest_width, overlay):
            ratio = dest_width / overlay.shape[1]
            dimension = (dest_width, int(overlay.shape[0] * ratio))
            return cv2.resize(overlay, dimension, interpolation = cv2.INTER_AREA)

        def calc_position(x, y, overlay):
            x_offset= x
            y_offset= y + int(overlay.shape[0] / 2)
            y1, y2 = y_offset, y_offset + overlay.shape[0]
            x1, x2 = x_offset, x_offset + overlay.shape[1]
            return x1, y1, x2, y2

        def overlay_with_alpha(x1, y1, x2, y2, overlay, background):
            alpha_over = overlay[:, :, 3] / 255.0
            alpha_bg = 1.0 - alpha_over

            for c in range(0, 3):
                background[y1:y2, x1:x2, c] = (alpha_over * overlay[:, :, c] +
                                          alpha_bg * background[y1:y2, x1:x2, c])
            return background

        for (x, y, w, h) in coords:
            resized = resize_overlay(w, overlay)
            x1,y1,x2,y2 = calc_position(x,y, resized)
            input = overlay_with_alpha(x1, y1, x2, y2, resized, input)
        return input

    def identify_prep(self, input):
        grayImage = cv2.cvtColor(input, cv2.COLOR_BGR2GRAY)
        return grayImage

    # Find eyes
    def identify_features(self, input):
        prepped_img = self.identify_prep(input)
        eye_cascade = cv2.CascadeClassifier(self.resources + '/' + self.identifier)
        eyes = eye_cascade.detectMultiScale(prepped_img)
        return eyes

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
    filterClass = laserEyes()
    filterClass.apply_filter(originalImg, debug=True)
