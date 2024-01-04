import os
import pygame
import sqlite3

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
    db = sqlite3.connect(database='./data/database/olympicsDB.db')
    return db


def selData(request):
    print(request, "\n")
    db = connectBD()
    requestExecutor = db.cursor()
    requestExecutor.execute(request)
    valuesList = requestExecutor.fetchall()

    for columnTitle in requestExecutor.description:
        print(f"{columnTitle[0]:35}", end="")
    print("\n")

    for rows in valuesList:
        for val in rows:
            print(f"{val:35}", end='')
        print()

    requestExecutor.close()
    db.close()

