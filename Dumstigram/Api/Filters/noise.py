import random
import tempfile
import numpy as np
import cv2


class noise(object):

    def filter_image(self, input, coords=None):
        def noisy(noise_typ, image):
            if noise_typ == "gauss":
                row, col, ch = image.shape
                mean = 0
                var = 2000
                sigma = var**0.5
                gauss = np.random.normal(mean, sigma, (row, col, ch))
                gauss = gauss.reshape(row, col, ch)
                noisy = image + gauss
                return noisy
            elif noise_typ == "s&p":
                row, col, ch = image.shape
                s_vs_p = 0.5
                amount = random.uniform(0.7, 0.1)
                out = np.copy(image)
                # Salt mode
                num_salt = np.ceil(amount * image.size * s_vs_p)
                coords = [np.random.randint(0, i - 1, int(num_salt))
                          for i in image.shape]
                out[coords] = (1)

                # Pepper mode
                num_pepper = np.ceil(amount * image.size * (1. - s_vs_p))
                coords = [np.random.randint(0, i - 1, int(num_pepper))
                          for i in image.shape]
                out[coords] = (0)
                return out
            elif noise_typ == "poisson":
                vals = len(np.unique(image))
                vals = 0.6 ** np.ceil(np.log2(vals))
                noisy = np.random.poisson(image * vals) / float(vals)
                return noisy
            elif noise_typ == "speckle":
                row, col, ch = image.shape
                gauss = np.random.randn(row, col, ch)
                gauss = gauss.reshape(row, col, ch)
                noisy = image + image * gauss
                return noisy

        noisy_types = ['gauss', 'poisson', 'speckle']  # , 's&p']
        noisy_array = noisy(random.choice(noisy_types), input)
        return noisy_array

    def identify_features(self, input):
        return None

    def apply_filter(self, input, debug=False):
        original = cv2.imread(input)

        if debug:
            cv2.imshow('Original', original)
        coords = self.identify_features(original)
        filtered = self.filter_image(original, coords)

        if debug:
            cv2.imshow('Filter Applied noisy3', filtered)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        tfile, tpath = tempfile.mkstemp(".png")
        cv2.imwrite(tpath, filtered)
        return tpath


if __name__ == '__main__':
    originalImg = '../uploads/test.png'
    filterClass = noise()
    filterClass.apply_filter(originalImg, debug=True)
