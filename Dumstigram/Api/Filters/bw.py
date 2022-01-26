import cv2

GRAY_MIDPOINT = 127
BLACK = 255


def filter_image(input, coords=None):
    grayImage = cv2.cvtColor(input, cv2.COLOR_BGR2GRAY)
    (_, blackAndWhiteImage) = cv2.threshold(grayImage,
                                            GRAY_MIDPOINT,
                                            BLACK,
                                            cv2.THRESH_BINARY)
    return blackAndWhiteImage


def identify_features(input):
    return None


def apply_filter(self, input, debug=False):
    print('Applying filter')
    print(self.get_info())
    original = cv2.imread(input)

    if debug:
        cv2.imshow('Original', original)
    coords = identify_features(original)
    filtered = filter_image(original, coords)

    if debug:
        cv2.imshow('Filter Applied', filtered)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return filtered


if __name__ == '__main__':
    originalImg = '../uploads/me.PNG'
    apply_filter(originalImg, debug=True)
