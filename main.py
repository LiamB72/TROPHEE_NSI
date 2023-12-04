from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets, QtGui,uic
from PyQt5.QtCore import QObject, pyqtSignal
import qdarkstyle
import pygame
import sys
from scripts.entities import entityPhysics
from scripts.utility import img_loader, load_img


"""
class MainWindows(QMainWindow):

    def __init__(self):
        super(MainWindows, self).__init__()
        uic.loadUi("data/main_menu.ui", self)
        self.setFixedSize(self.size())
        self.show()

        self.startButton.clicked.connect(self.startGame())
        self.optionButton.clicked.connect(self.optionMenu())
        self.quitButton.clicked.connect(self.quitGame())

    def startGame(self):
        pass

    def optionMenu(self):
        pass

    def quitGame(self):
        pass

# app = QApplication(sys.argv)
# window = MainWindows()
# app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
# app.exec_()
"""
pygame.init()

class gameProgram:
    def __init__(self):

        pygame.display.set_caption("In development!")
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((240, 180))
        self.font = pygame.font.SysFont("Courier New", 15)

        self.clock = pygame.time.Clock()

        self.x_mov = [False, False]
        self.y_mov = [False, False]

        self.player = entityPhysics(self, 'player', (50, 50), (8, 15))

        self.assets = {
            'player': img_loader('entities/player/player.png')
        }

    def run(self):

        while True:
            self.display.fill((0, 0, 0))
            showText = self.font.render(f"fps: {self.clock.get_fps():.0f}", False, (255, 255, 255))
            self.display.blit(showText, (15, 15))

            self.player.update((self.x_mov[1] - self.x_mov[0], 0))
            self.player.update((0, self.y_mov[1] - self.y_mov[0]))
            self.player.render(self.display)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.x_mov[0] = True
                    if event.key == pygame.K_d:
                        self.x_mov[1] = True
                    if event.key == pygame.K_z:
                        self.y_mov[0] = True
                    if event.key == pygame.K_s:
                        self.y_mov[1] = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_q:
                        self.x_mov[0] = False
                    if event.key == pygame.K_d:
                        self.x_mov[1] = False
                    if event.key == pygame.K_z:
                        self.y_mov[0] = False
                    if event.key == pygame.K_s:
                        self.y_mov[1] = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)


gameProgram().run()
