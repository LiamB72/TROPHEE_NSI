"""
File Created By BERGE Liam
Created on 2023-12-05
Last Update on 2024-01-25
"""
import os
import pygame
import sqlite3

BASE_IMG_PATH = 'data/images/'


def img_loader(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))

    return img


def load_imgs(path):
    images = []
    for img_name in os.listdir(BASE_IMG_PATH + path):
        images.append(img_loader(path + '/' + img_name))
    return images

def selData(request):
    print(request, "\n")
    db = sqlite3.connect(database='./data/database/olympicsDB.db')
    requestExecutor = db.cursor()
    requestExecutor.execute(request)
    valuesList = requestExecutor.fetchall()
    titleRow = []
    dataRows = []
    for columnTitle in requestExecutor.description:
        titleRow.append(columnTitle[0])

    for rows in valuesList:
        for values in rows:
            dataRows.append(values)

    requestExecutor.close()
    db.close()
    return titleRow, dataRows

