import random
import numpy as np
if __name__ == '__main__':
    import sys
    sys.path.append('../models')
    from basic_filter import basic_filter
else:
    from models.basic_filter import basic_filter


class noise(basic_filter):
    def __init__(self, debug=False):
        super().__init__(debug)
        self.friendly_name = 'Noise'
        self.description = """Adds random forms of image noise"""
        self.example_url = 'https://people.sc.fsu.edu/~jburkardt/c_src/image_denoise/balloons_noisy.png'
        self.randomization = ['noise method', 's vs p amount']
        self.performance_impact = 2

    def filter_image(self, input):
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
        chosen_noise = random.choice(noisy_types)
        if self.debug:
            print('Applying {} noise'.format(chosen_noise))
        noisy_array = noisy(chosen_noise, input)
        return noisy_array


if __name__ == '__main__':
    originalImg = '../uploads/test.png'
    filterClass = noise(debug=True)
    filterClass.apply_filter(originalImg)
