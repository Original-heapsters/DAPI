import os
import tempfile
import cv2
import random


class cryLaughing(object):
    def __init__(self):
        dirname = os.path.dirname(__file__)
        self.additives = os.path.join(dirname, 'additives')

    def get_info(self):
        return {
                'name': __class__.__name__,
                'description': """Places a cry laughing emoji on the source""",
                'randomized_aspects': ['Location'],
                'performance_impact': 1,
                'requires_face': False,
                }

    def filter_image(self, input):
        overlay = cv2.imread(self.additives + '/cry_laughing.png', -1)
        height, width, channels = input.shape
        overlay = cv2.resize(overlay, (width, height), interpolation=cv2.INTER_AREA)

        print(input.shape)
        print(overlay.shape)

        # def resize_overlay(dest_width, overlay):
        #     ratio = dest_width / overlay.shape[1]
        #     dimension = (dest_width, int(overlay.shape[0] * ratio))
        #     return cv2.resize(overlay, dimension, interpolation=cv2.INTER_AREA)
        #
        # def overlay_with_alpha(x1, y1, x2, y2, overlay, background):
        #     alpha_over = overlay[:, :, 3] / 255.0
        #     alpha_bg = 1.0 - alpha_over
        #
        #     for c in range(0, 3):
        #         background[y1:y2, x1:x2, c] = (alpha_over * overlay[:, :, c] +
        #                                        alpha_bg * background[y1:y2,
        #                                        x1:x2,
        #                                        c])
        #     return background

        added_image = cv2.addWeighted(input, 0.3, overlay, 0.7, 0.0)
        return added_image

    def identify_prep(self, input):
        return None

    # Find eyes
    def identify_features(self, input):
        return None

    def apply_filter(self, input, debug=False):
        print('Applying filter')
        print(self.get_info())
        original = cv2.imread(input)

        if debug:
            cv2.imshow('Original', original)
        filtered = self.filter_image(original)

        if debug and filtered is not None:
            cv2.imshow('Filter Applied', filtered)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        tfile, tpath = tempfile.mkstemp(".png")
        cv2.imwrite(tpath, filtered)
        return tpath


if __name__ == '__main__':
    originalImg = '../uploads/test.png'
    filterClass = cryLaughing()
    filterClass.apply_filter(originalImg, debug=True)
