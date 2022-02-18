import numpy as np
from keras.preprocessing import image


def load_img_and_resize(img_path, size):
    img = image.load_img(img_path)
    img = img.resize(size=size)
    return img


def image_sim(img1, img2):
    vec1 = np.array(img1).flatten() / 255
    vec2 = np.array(img2).flatten() / 255
    dist = np.linalg.norm(vec1 - vec2)
    sim = 1.0 - dist/(vec1.shape[0]**0.5)
    return sim
