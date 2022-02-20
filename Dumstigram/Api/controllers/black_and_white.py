import cv2
from models.basic_filter import basic_filter


GRAY_MIDPOINT = 127
BLACK = 255


class black_and_white(basic_filter):
    def __init__(self, debug=False):
        super().__init__(debug)
        self.description = """Black and white filter"""

    def filter_image(self, input):
        grayImage = cv2.cvtColor(input, cv2.COLOR_BGR2GRAY)
        (_, blackAndWhiteImage) = cv2.threshold(grayImage,
                                                GRAY_MIDPOINT,
                                                BLACK,
                                                cv2.THRESH_BINARY)
        return blackAndWhiteImage


if __name__ == '__main__':
    originalImg = '../uploads/test.png'
    filterClass = black_and_white(debug=True)
    filterClass.apply_filter(originalImg)
