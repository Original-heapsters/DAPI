import tempfile
import cv2
from .basic_filter import basic_filter


class overlay_filter(basic_filter):
    def __init__(self, debug=False):
        super().__init__(debug)
        self.description = """Most basic filter to apply an overlay to an image
                              this just returns the input image"""
        self.additives = '.'

    def get_info(self):
        return {
                'name': self.__class__.__name__,
                'description': self.description,
                'randomized_aspects': self.randomization,
                'performance_impact': self.performance,
                'requires_face': self.requires_detection,
                'debug_mode': self.debug,
                }

    def resize_overlay(self, dest_width, overlay):
        ratio = dest_width / overlay.shape[1]
        dimension = (dest_width, int(overlay.shape[0] * ratio))
        return cv2.resize(overlay, dimension, interpolation=cv2.INTER_AREA)

    def calc_position(self, x, y, overlay):
        # Define bounding diagonal points for overlay
        y1, y2 = y, y + overlay.shape[0]
        x1, x2 = x, x + overlay.shape[1]
        return x1, y1, x2, y2

    def overlay_with_alpha(self, x1, y1, x2, y2, overlay, background):
        alpha_over = overlay[:, :, 3] / 255.0
        alpha_bg = 1.0 - alpha_over

        for c in range(0, 3):
            background[y1:y2, x1:x2, c] = (alpha_over * overlay[:, :, c] +
                                           alpha_bg * background[y1:y2,
                                           x1:x2,
                                           c])
        return background

    def filter_image(self, input):
        raise NotImplementedError

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
    filterClass = overlay_filter(debug=True)
    filterClass.apply_filter(originalImg)
