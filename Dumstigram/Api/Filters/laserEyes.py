import cv2
import random

RESOURCES = './resources'
ADDITIVES = './additives'
LASER_COUNT = 5
IDENTIFIER = 'haar_eye_tree_glasses.xml'
def filter_image(input, coords=None):
    if coords is None:
        return None

    filtered = input

    laser_chosen = 'laser_' + str(random.randint(1,LASER_COUNT))
    overlay = cv2.imread(ADDITIVES + '/' + laser_chosen + '.png', -1)

    l_img = filtered
    for (x, y, w, h) in coords:
        r = w / overlay.shape[1]
        dim = (w, int(overlay.shape[0] * r))
        s_img = cv2.resize(overlay, dim, interpolation = cv2.INTER_AREA)

        x_offset= x
        y_offset= y + int(s_img.shape[0] / 2)
        y1, y2 = y_offset, y_offset + s_img.shape[0]
        x1, x2 = x_offset, x_offset + s_img.shape[1]

        alpha_s = s_img[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s

        for c in range(0, 3):
            l_img[y1:y2, x1:x2, c] = (alpha_s * s_img[:, :, c] +
                                      alpha_l * l_img[y1:y2, x1:x2, c])
    return l_img

def identify_prep(input):
    grayImage = cv2.cvtColor(input, cv2.COLOR_BGR2GRAY)
    return grayImage

# Find eyes
def identify_features(input):
    prepped_img = identify_prep(input)
    eye_cascade = cv2.CascadeClassifier(RESOURCES + '/' + IDENTIFIER)
    eyes = eye_cascade.detectMultiScale(prepped_img)
    return eyes

def apply_filter(input, debug=False):
    original = cv2.imread(input)

    if debug:
        cv2.imshow('Original', original)
    coords = identify_features(original)
    filtered = filter_image(original, coords)

    if debug and filtered is not None:
        cv2.imshow('Filter Applied', filtered)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return filtered


if __name__ == '__main__':
    originalImg = '../uploads/test.png'
    apply_filter(originalImg, debug=True)
