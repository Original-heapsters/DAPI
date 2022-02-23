import os
import tempfile
import cv2
import random


class mustache(object):
    def __init__(self,
                 smile_cascade=None,
                 face_cascade=None):
        dirname = os.path.dirname(__file__)
        self.resources = os.path.join(dirname, 'resources')
        self.additives = os.path.join(dirname, 'additives')
        self.laser_count = 5
        self.mouth_cascade = smile_cascade
        self.face_cascade = face_cascade

    def get_info(self):
        return {
                'name': __class__.__name__,
                'description': """Add random set of lasers on detected eyes""",
                'randomized_aspects': ['laser chosen'],
                'performance_impact': 2,
                'requires_face': True,
                }

    def filter_image(self, input, coords=None):
        if coords is None:
            return input

        overlay = cv2.imread(self.additives + '/mustache.png', -1)

        def resize_overlay(dest_width, overlay):
            ratio = dest_width / overlay.shape[1]
            dimension = (dest_width, int(overlay.shape[0] * ratio))
            return cv2.resize(overlay, dimension, interpolation=cv2.INTER_AREA)

        def calc_position(x, y, overlay):
            x_offset = x
            y_offset = y - int(overlay.shape[0] / 4)
            y1, y2 = y_offset, y_offset + overlay.shape[0]
            x1, x2 = x_offset, x_offset + overlay.shape[1]
            return x1, y1, x2, y2

        def overlay_with_alpha(x1, y1, x2, y2, overlay, background):
            alpha_over = overlay[:, :, 3] / 255.0
            alpha_bg = 1.0 - alpha_over

            for c in range(0, 3):
                background[y1:y2, x1:x2, c] = (alpha_over * overlay[:, :, c] +
                                               alpha_bg * background[y1:y2,
                                               x1:x2,
                                               c])
            return background

        for (x, y, w, h) in coords:
            print('OVERLAY START')
            print(coords)
            resized = resize_overlay(w, overlay)
            x1, y1, x2, y2 = calc_position(x, y, resized)
            input = overlay_with_alpha(x1, y1, x2, y2, resized, input)
        return input

    def identify_prep(self, input):
        grayImage = cv2.cvtColor(input, cv2.COLOR_BGR2GRAY)
        return grayImage

    # Find mouth
    def identify_features(self, input):
        prepped_img = self.identify_prep(input)
        # classifier = os.path.join(self.resources, self.identifier)
        # classifier_face = os.path.join(self.resources, self.identifier_face)
        # face_cascade = cv2.CascadeClassifier(classifier_face)
        # mouth_cascade = cv2.CascadeClassifier(classifier)
        # smile = mouth_cascade.detectMultiScale(prepped_img)
        faces = self.face_cascade.detectMultiScale(prepped_img, 1.3, 5)
        print('faces are')
        print(faces)
        for (x, y, w, h) in faces:
            # cv2.rectangle(input, (x, y), ((x + w), (y + h)), (255, 0, 0), 2)
            roi_gray = prepped_img[y:y + h, x:x + w]
            input = input[y:y + h, x:x + w]
            smiles = self.mouth_cascade.detectMultiScale(roi_gray, 1.8, 20)
            coords = []
            for (sx, sy, sw, sh) in smiles:
                # cv2.rectangle(input, (sx, sy), ((sx + sw), (sy + sh)), (0, 0, 255), 2)
                coords.append([sx+x, sy+y, sw, sh])
        return coords

    def apply_filter(self, input, debug=False):
        print('Applying filter')
        print(self.get_info())
        original = cv2.imread(input)

        if debug:
            cv2.imshow('Original', original)
        coords = self.identify_features(original)
        print('***********************')
        print(coords)
        print('***********************')
        # cv2.rectangle(coords[0])
        x = coords[0][0]
        y = coords[0][1]
        w = coords[0][2]
        h = coords[0][3]

        # original = cv2.rectangle(original, (x, y), (x + w, y + h), (255, 0, 0), 1)
        filtered = self.filter_image(original, coords)

        if debug and filtered is not None:
            cv2.imshow('Filter Applied', filtered)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        tfile, tpath = tempfile.mkstemp(".png")
        cv2.imwrite(tpath, filtered)
        return tpath


if __name__ == '__main__':
    originalImg = '../uploads/smileLady.jpg'
    filterClass = mustache()
    filterClass.apply_filter(originalImg, debug=True)
