"""
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets, QtGui,uic
from PyQt5.QtCore import QObject, pyqtSignal
import qdarkstyle
"""
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
        #Initialises the pygame basic window configs
        pygame.display.set_caption("Trophy NSI")
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((480, 360))
        self.font = pygame.font.SysFont("Courier New", 18)

        self.clock = pygame.time.Clock() #Fps variable

        self.x_mov = [False, False] # Used to check left and right key detection
        self.y_mov = [False, False] # Same but for the up and down

        # You can see the code for it in the entities.py file
        self.player = entityPhysics(self, 'player', (212, 154), (28, 26))

        #dict so it's easier to load images.
        self.assets = {
            'player': img_loader('entities/player/perso.png'),
        }

        # Actual Rect, holy hell.
        self.rectTest = pygame.Rect(325, 175, 125, 150)

    def run(self):

        while True:
            self.display.fill((0, 0, 0)) # Renders the screen black

            # Shows the current fps
            fpsText = self.font.render(f"fps: {self.clock.get_fps():.0f}", False, (255, 255, 255))
            playerPosText = self.font.render(f"Pos: {self.player.entity_pos[0]:.2f}, {self.player.entity_pos[1]:.2f}",
                                             False, (255, 255, 255))
            self.display.blit(fpsText, (15, 25))
            self.display.blit(playerPosText, (15, 45))



            # Creates&Updates the rect of the player's, basically it's collision/bonding box.
            playerRect = pygame.Rect(self.player.entity_pos[0], self.player.entity_pos[1], self.player.size[0], self.player.size[1])

            # Draws the two rect box on the display
            pygame.draw.rect(self.display, (100,100,100), self.rectTest)
            pygame.draw.rect(self.display, (0,0,0), playerRect)

            # See code in entities.py
            self.player.update(((self.x_mov[1] - self.x_mov[0])*1.257, 0))
            self.player.update((0, (self.y_mov[1] - self.y_mov[0])*1.257))
            self.player.render(self.display)

            # Checks for the collision between the rectTest and the player's collision box.
            if pygame.Rect.colliderect(self.rectTest, playerRect):
                pygame.draw.rect(self.display, (255, 255, 255), self.rectTest)

            # Checks for key press !!! You can change to your heart desire !!!
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # When key pressed
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.x_mov[0] = True
                    if event.key == pygame.K_d:
                        self.x_mov[1] = True
                    if event.key == pygame.K_z:
                        self.y_mov[0] = True
                    if event.key == pygame.K_s:
                        self.y_mov[1] = True

                # When key released
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_q:
                        self.x_mov[0] = False
                    if event.key == pygame.K_d:
                        self.x_mov[1] = False
                    if event.key == pygame.K_z:
                        self.y_mov[0] = False
                    if event.key == pygame.K_s:
                        self.y_mov[1] = False

            # Makes the display on a bigger scale due to pixel art.
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))

            # Obviously.
            pygame.display.update()
            self.clock.tick(60)

gameProgram().run()
