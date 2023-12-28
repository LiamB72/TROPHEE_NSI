import os
import mysql.connector
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


def connectBD():
    db = mysql.connector.connect(user='root', password='',
                                 host='127.0.0.1',
                                 database='olympicsDB')
    return db


def selectData(request):
    value = ""
    db = connectBD()
    requestExecutor = db.cursor()
    requestExecutor.execute(request)
    valuesList = requestExecutor.fetchall()

    for rows in valuesList:
        for val in rows:
            value += str(val) + "; "

    requestExecutor.close()
    db.close()
    return value