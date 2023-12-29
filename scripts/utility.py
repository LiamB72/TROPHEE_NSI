import os
import pygame

BASE_IMG_PATH = 'data/images/'


def img_loader(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))

    return img


def load_img(path):
    images = []
    for img_name in os.listdir(BASE_IMG_PATH + path):
        images.append(img_loader(path + '/' + img_name))
    return images
