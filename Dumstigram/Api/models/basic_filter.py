import tempfile
import cv2


class basic_filter(object):
    def __init__(self, debug=False):
        self.description = """Most basic filter to apply to an image
                              this just returns the input image"""
        self.randomization = []
        self.performance = 1
        self.requires_detection = False
        self.debug = debug

    def get_info(self):
        return {
                'name': self.__class__.__name__,
                'description': self.description,
                'randomized_aspects': self.randomization,
                'performance_impact': self.performance,
                'requires_face': self.requires_detection,
                'debug_mode': self.debug,
                }

    def filter_image(self, input):
        return input

    def write_temp_file(self, input):
        tfile, temp_path = tempfile.mkstemp(".png")
        cv2.imwrite(temp_path, input)
        return temp_path

    def apply_filter(self, input):
        name = self.get_info()['name']

        print('Applying filter {}'.format(name))
        original = cv2.imread(input)
        filtered = self.filter_image(original)
        finished_image = filtered if filtered is not None else original

        if self.debug:
            print(self.get_info())
            cv2.imshow('Original', original)

            if filtered is not None:
                window_title = '{} Filter Applied'.format(name)
            else:
                window_title = '{} Filter Failed'.format(name)
            cv2.imshow(window_title, finished_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        path_to_filtered = self.write_temp_file(finished_image)
        return path_to_filtered


if __name__ == '__main__':
    originalImg = '../uploads/test.png'
    filterClass = basic_filter(debug=True)
    filterClass.apply_filter(originalImg)
