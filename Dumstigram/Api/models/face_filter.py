import os
import tempfile
import cv2
from .basic_filter import basic_filter


class face_filter(basic_filter):
    def __init__(self,
                 eye_cascade=None,
                 smile_cascade=None,
                 face_cascade=None,
                 mode='eyes',
                 debug=False):
        super().__init__(debug)
        self.description = """Most basic filter based around facial detection
                              this just returns the input image"""
        self.eye_cascade = eye_cascade
        self.smile_cascade = smile_cascade
        self.face_cascade = face_cascade
        self.detection_mode = mode
        self.requires_detection = True

    def get_info(self):
        return {
                'name': self.__class__.__name__,
                'description': self.description,
                'randomized_aspects': self.randomization,
                'performance_impact': self.performance,
                'requires_face': self.requires_detection,
                'eye_cascade': self.eye_cascade,
                'smile_cascade': self.smile_cascade,
                'face_cascade': self.face_cascade,
                'detection_mode': self.detection_mode,
                'debug_mode': self.debug,
                }

    def filter_image(self, input, coords=None):
        raise NotImplementedError

    def identify_prep(self, input):
        grayImage = cv2.cvtColor(input, cv2.COLOR_BGR2GRAY)
        return grayImage

    def debug_rects(self, input, coords):
        if not self.debug:
            return

        for (x, y, w, h) in coords:
            cv2.rectangle(input, (x, y), ((x + w), (y + h)), (255, 0, 0), 2)

    def identify_features(self, input):
        prepped_img = self.identify_prep(input)
        if self.detection_mode == 'eyes':
            eyes = self.eye_cascade.detectMultiScale(prepped_img)
            self.debug_rects(input, eyes)
            return eyes
        elif self.detection_mode == 'face':
            faces = self.face_cascade.detectMultiScale(prepped_img, 1.3, 5)
            self.debug_rects(input, faces)
            return faces
        elif self.detection_mode == 'smile':
            faces = self.face_cascade.detectMultiScale(prepped_img, 1.3, 5)
            smile_coords = []
            for (x, y, w, h) in faces:
                roi_gray = prepped_img[y:y + h, x:x + w]
                smiles = self.smile_cascade.detectMultiScale(roi_gray, 1.8, 20)
                for (sx, sy, sw, sh) in smiles:
                    smile_coords.append([sx+x, sy+y, sw, sh])
            self.debug_rects(input, smile_coords)
            return smile_coords

    def apply_filter(self, input):
        print('Applying filter')
        print(self.get_info())
        original = self.resize_max_width(input)

        if self.debug:
            cv2.imshow('Original', original)
        coords = self.identify_features(original)
        filtered = self.filter_image(original, coords)

        if self.debug and filtered is not None:
            cv2.imshow('Filter Applied', filtered)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        tfile, tpath = tempfile.mkstemp(".png")
        cv2.imwrite(tpath, filtered)
        return tpath


if __name__ == '__main__':
    eye_classifier = os.path.join('./resources',
                                  'haar_eye_tree_glasses.xml')
    eye_cascade = cv2.CascadeClassifier(eye_classifier)
    face_classifier = os.path.join('./resources',
                                   'haarcascade_frontalface_default.xml')
    face_cascade = cv2.CascadeClassifier(face_classifier)
    smile_classifier = os.path.join('./resources',
                                    'haarcascade_smile.xml')
    smile_cascade = cv2.CascadeClassifier(smile_classifier)
    originalImg = '../uploads/test.png'
    filterClass = face_filter(eye_cascade,
                              smile_cascade,
                              face_cascade,
                              mode='eyes',
                              debug=True)
    filterClass.apply_filter(originalImg)
