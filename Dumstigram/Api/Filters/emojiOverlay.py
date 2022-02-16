import os
import tempfile
import cv2
import random


class emojiOverlay(object):
    def __init__(self):
        dirname = os.path.dirname(__file__)
        self.additives = os.path.join(dirname, 'additives')

    def get_info(self):
        return {
                'name': __class__.__name__,
                'description': """Places a random emoji on the source""",
                'randomized_aspects': ['Location'],
                'performance_impact': 1,
                'requires_face': False,
                }

    def filter_image(self, input):

        emoji_chosen = random.choice(['cry_laughing', 'hunnit', 'ok'])
        overlay = cv2.imread(self.additives + '/' + emoji_chosen + '.png', -1)

        def resize_overlay(dest_width, overlay):
            ratio = dest_width / overlay.shape[1]
            dimension = (dest_width, int(overlay.shape[0] * ratio))
            return cv2.resize(overlay, dimension, interpolation=cv2.INTER_AREA)

        def calc_position(x, y, overlay):
            # Define bounding diagonal points for overlay
            y1, y2 = y, y + overlay.shape[0]
            x1, x2 = x, x + overlay.shape[1]
            return x1, y1, x2, y2

        def overlay_with_alpha(x1, y1, x2, y2, overlay, background):
            alpha_over = overlay[:, :, 3] / 255.0
            alpha_bg = 1.0 - alpha_over

            for c in range(0, 3):
                background[y1:y2, x1:x2, c] = (alpha_over * overlay[:, :, c] +
                                               alpha_bg * background[y1:y2,
                                               x1:x2,
                                               c])
            return background

        min_width = int(input.shape[0] / 8)
        max_width = int(input.shape[0] / 2)
        target_width = random.randint(min_width, max_width)
        resized = resize_overlay(target_width, overlay)

        # X: 0 -> anywhere within the width (minus width of overlay)
        # Y: 0 -> anywhere within the height (minus height of *resized overlay)
        target_x = random.randint(0, input.shape[1] - target_width)
        target_y = random.randint(0, input.shape[0] - resized.shape[0])

        x1, y1, x2, y2 = calc_position(target_x, target_y, resized)
        input = overlay_with_alpha(x1, y1, x2, y2, resized, input)
        return input

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
    filterClass = emojiOverlay()
    filterClass.apply_filter(originalImg, debug=True)
