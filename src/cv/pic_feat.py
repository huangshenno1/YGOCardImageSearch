import numpy as np
from numpy import linalg

from keras.preprocessing import image
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input


class PicFeat:
    CARD_WIDTH = 322
    CARD_HEIGHT = 470

    def __init__(self):
        image_shape = (PicFeat.CARD_HEIGHT, PicFeat.CARD_WIDTH, 3)
        weights = 'imagenet'
        pooling = 'max'
        self.model = VGG16(input_shape=(image_shape[0], image_shape[1], image_shape[2]),
                           weights=weights,
                           pooling=pooling,
                           include_top=False)

    def process_file(self, img_path):
        img = image.load_img(img_path)
        return self.process(img)

    def process(self, img):
        img = img.resize(size=(PicFeat.CARD_WIDTH, PicFeat.CARD_HEIGHT))
        img = image.img_to_array(img)
        img = np.expand_dims(img, axis=0)
        img = preprocess_input(img)
        feat = self.model.predict(img)
        norm_feat = feat[0] / linalg.norm(feat[0])
        return norm_feat
