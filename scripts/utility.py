"""
File Created By BERGE Liam
Created on 2023-12-05
Last Update on 2024-01-25
"""
import os
import pygame
import sqlite3

BASE_IMG_PATH = 'data/images/'


def img_loader(path) -> pygame.image:
    """data/images/{path}
    Loads the single image from the path.
    need to specify the image to load, with both the name and extension of the file."""
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    img = pygame.transform.scale(img, (img.get_width() // 2, img.get_height() // 2))

    return img


def load_imgs(path) -> list[pygame.image]:
    """data/images/{path}
    Then loads the differents images found within the specified directory.
    also, no need to add the '/' at the end, to specify the directory."""
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

