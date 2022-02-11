import os
import tempfile
import cv2
import random


class circle(object):
    def __init__(self, eye_cascade=None):
        self.eye_cascade = eye_cascade
        self.detection_mode = 'eyes'
        self.circle_count = 5
        self.identifier = 'haar_eye_tree_glasses.xml'

    def get_info(self):
        return {
                'name': __class__.__name__,
                'description': """Places red cirle around eyes""",
                'randomized_aspects': [],
                'performance_impact': 3,
                'requires_face': True,
                }

    def filter_image(self, input, coords=None):
        if coords is None or len(coords) == 0:
            return input

        for pts in coords:
            rect_center = (pts[0] + int(pts[2]/2), pts[1] + int(pts[3]/2))
            red = (0, 0, 255)
            if random.randint(0, 1) == 0:
                # 50/50 chance to draw a cirlce for every detected eye
                cv2.circle(input,
                           rect_center,
                           random.randint(1, pts[3]),
                           red,
                           random.randint(2, 5))
        return input

    def identify_prep(self, input):
        grayImage = cv2.cvtColor(input, cv2.COLOR_BGR2GRAY)
        return grayImage

    # Find eyes
    def identify_features(self, input):
        prepped_img = self.identify_prep(input)
        if self.detection_mode == 'eyes':
            eyes = self.eye_cascade.detectMultiScale(prepped_img)
            return eyes
        elif self.detection_mode == 'smile':  # Experimental, does not work
            faces = self.face_cascade.detectMultiScale(prepped_img, 1.3, 5)
            smiles = []
            for (x, y, w, h) in faces:
                smiles.append(self.smile_cascade.detectMultiScale(prepped_img,
                                                                  1.8,
                                                                  20))
            return smiles

    def apply_filter(self, input, debug=False):
        print('Applying filter')
        print(self.get_info())
        original = cv2.imread(input)

        if debug:
            cv2.imshow('Original', original)
        coords = self.identify_features(original)
        filtered = self.filter_image(original, coords)

        if debug and filtered is not None:
            cv2.imshow('Filter Applied', filtered)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        tfile, tpath = tempfile.mkstemp(".png")
        cv2.imwrite(tpath, filtered)
        return tpath


if __name__ == '__main__':
    classifier = os.path.join('./resources',
                              'haar_eye_tree_glasses.xml')
    eye_cascade = cv2.CascadeClassifier(classifier)
    originalImg = '../uploads/test.png'
    filterClass = circle(eye_cascade)
    filterClass.apply_filter(originalImg, debug=True)
