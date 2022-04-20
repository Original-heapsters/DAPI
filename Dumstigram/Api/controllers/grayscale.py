import cv2
if __name__ == '__main__':
    import sys
    sys.path.append('../models')
    from basic_filter import basic_filter
else:
    from models.basic_filter import basic_filter


class grayscale(basic_filter):
    def __init__(self, debug=False):
        super().__init__(debug)
        self.friendly_name = 'Grayscale'
        self.description = """Grayscale filter"""
        self.example_url = 'https://i0.wp.com/techtutorialsx.com/wp-content/uploads/2019/04/image-7.png?w=831&ssl=1'

    def filter_image(self, input):
        grayImage = cv2.cvtColor(input, cv2.COLOR_BGR2GRAY)
        return grayImage


if __name__ == '__main__':
    originalImg = '../uploads/test.png'
    filterClass = grayscale(debug=True)
    filterClass.apply_filter(originalImg)
