import cv2
import random
if __name__ == '__main__':
    import sys
    sys.path.append('../models')
    from basic_filter import basic_filter
else:
    from models.basic_filter import basic_filter


TOP_TEXT = ['Top Text',
            'When you',
            'How it feels',
            'How I feel',
            'That feeling',
            'Hold up']

BOTTOM_TEXT = ['Bottom Text',
               'When you',
               'When I',
               'After',
               'When',
               'When the bass',
               'Epic',
               'That feeling']


class add_text(basic_filter):
    def __init__(self, is_top_text=True, debug=False):
        super().__init__(debug)
        self.friendly_name = 'Top Text' if is_top_text else 'Bottom Text'
        self.description = """Adds top text"""
        self.example_url = 'https://dh2020.adho.org/wp-content/uploads/2020/07/schmidt_590_figure1.jpg'
        self.is_top_text = is_top_text

    def filter_image(self, input):
        print(input.shape)
        x = int(input.shape[0] / 2)
        y = int(input.shape[1] / 8)
        text_chosen = random.choice(TOP_TEXT)

        if not self.is_top_text:
            y = int(input.shape[1] / 2)
            text_chosen = random.choice(BOTTOM_TEXT)

        cv2.putText(img=input,
                    text=text_chosen,
                    org=(x, y),
                    fontFace=cv2.FONT_HERSHEY_COMPLEX,
                    fontScale=0.75,
                    color=[0, 0, 0],
                    lineType=cv2.LINE_AA,
                    thickness=8)
        cv2.putText(img=input,
                    text=text_chosen,
                    org=(x, y),
                    fontFace=cv2.FONT_HERSHEY_COMPLEX,
                    fontScale=0.75,
                    color=[255, 255, 255],
                    lineType=cv2.LINE_AA,
                    thickness=2)

        return input


if __name__ == '__main__':
    import sys
    sys.path.append('../models')
    originalImg = '../uploads/test.png'
    filterClass = add_text(is_top_text=False, debug=True)
    filterClass.apply_filter(originalImg)
