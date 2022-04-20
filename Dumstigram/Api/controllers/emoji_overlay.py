import os
import cv2
import random
if __name__ == '__main__':
    import sys
    sys.path.append('../models')
    from overlay_filter import overlay_filter
else:
    from models.overlay_filter import overlay_filter


class emoji_overlay(overlay_filter):
    def __init__(self, debug=False):
        super().__init__(debug)
        self.friendly_name = 'Emoji Overlay'
        self.description = """Places a random emoji on the source"""
        self.example_url = 'https://pics.me.me/thumb_deep-fried-meme-starter-pack-100-%D0%B2-%D0%B2%D0%B5%D1%81%D0%B0use-these-emojies-lens-66226636.png'
        self.randomization = ['Location']
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        self.additives = os.path.join(curr_dir, 'emojis')

    def filter_image(self, input):
        emoji_chosen = random.choice(os.listdir(self.additives))
        overlay = cv2.imread(self.additives + '/' + emoji_chosen, -1)

        min_width = int(input.shape[0] / 8)
        max_width = int(input.shape[0] / 2)
        target_width = random.randint(min_width, max_width)
        resized = self.resize_overlay(target_width, overlay)

        # X: 0 -> anywhere within the width (minus width of overlay)
        # Y: 0 -> anywhere within the height (minus height of *resized overlay)
        target_x = random.randint(0, input.shape[1] - target_width)
        target_y = random.randint(0, input.shape[0] - resized.shape[0])

        x1, y1, x2, y2 = self.calc_position(target_x, target_y, resized)
        input = self.overlay_with_alpha(x1, y1, x2, y2, resized, input)
        return input


if __name__ == '__main__':
    originalImg = '../uploads/test.png'
    filterClass = emoji_overlay(debug=True)
    filterClass.apply_filter(originalImg)
