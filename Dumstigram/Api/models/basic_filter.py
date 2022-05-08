import tempfile
import cv2


class basic_filter(object):
    def __init__(self, debug=False):
        self.name = self.__class__.__name__
        self.friendly_name = 'Basic filter'
        self.description = """Most basic filter to apply to an image
                              this just returns the input image"""
        self.example_url = 'https://answers.opencv.org/upfiles/14972594339956657.jpg'
        self.randomization = []
        self.performance = 1
        self.requires_detection = False
        self.source_filename = None
        self.debug = debug

    def get_info(self):
        return {
                'name': self.name,
                'description': self.description,
                'example_url': self.example_url,
                'friendly_name': self.friendly_name,
                'randomized_aspects': self.randomization,
                'performance_impact': self.performance,
                'requires_face': self.requires_detection,
                'debug_mode': self.debug,
                }

    def filter_image(self, input):
        raise NotImplementedError

    def write_temp_file(self, input):
        tfile, temp_path = tempfile.mkstemp(".png")
        cv2.imwrite(temp_path, input)
        return temp_path

    def resize_max_width(self, input_file, max_width=500):
        input = cv2.imread(input_file)
        ratio = max_width / input.shape[1]
        dimension = (max_width, int(input.shape[0] * ratio))
        return cv2.resize(input, dimension, interpolation=cv2.INTER_AREA)

    def apply_filter(self, input):
        self.source_filename = input
        name = self.get_info()['name']

        print('Applying filter {}'.format(name))
        original = self.resize_max_width(input)
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
