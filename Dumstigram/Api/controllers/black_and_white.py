import cv2
if __name__ == '__main__':
    import sys
    sys.path.append('../models')
    from basic_filter import basic_filter
else:
    from models.basic_filter import basic_filter


GRAY_MIDPOINT = 127
BLACK = 255


class black_and_white(basic_filter):
    def __init__(self, debug=False):
        super().__init__(debug)
        self.friendly_name = 'Black & White'
        self.description = """Black and white filter"""
        self.example_url = 'https://i0.wp.com/techtutorialsx.com/wp-content/uploads/2019/04/image-7.png?w=831&ssl=1'

    def filter_image(self, input):
        grayImage = cv2.cvtColor(input, cv2.COLOR_BGR2GRAY)
        (_, blackAndWhiteImage) = cv2.threshold(grayImage,
                                                GRAY_MIDPOINT,
                                                BLACK,
                                                cv2.THRESH_BINARY)
        return blackAndWhiteImage


if __name__ == '__main__':
    import sys
    sys.path.append('../models')
    originalImg = '../uploads/test.png'
    filterClass = black_and_white(debug=True)
    filterClass.apply_filter(originalImg)
