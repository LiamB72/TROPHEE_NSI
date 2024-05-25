"""
File Created By BERGE Liam & REEVES Guillaume
Graphics Made by Vix/Lucy (SCARPA Ayden)
Created on 2023-12-04
Last Updated on 2024-05-23
"""
import sys
import pygame
from scripts.playerModule import player
from scripts.utility import img_loader, load_imgs
from scripts.UIsModule import openUI, promptMenu

pygame.init()

class gameProgram:
    def __init__(self):
        # Initialises the pygame basic window configs
        pygame.display.set_caption("Les J.O. aux services des bases de données: Trophée NSI")
        pygame.display.set_icon(pygame.image.load("./data/images/icons/logo.png"))

        self.ratio_Factor = 1.5
        self.screen_width, self.screen_height = 600, 600
        self.display_width = self.screen_width // self.ratio_Factor
        self.display_height = self.screen_height // self.ratio_Factor

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.display = pygame.Surface((self.display_width, self.display_height))

        self.font = pygame.font.SysFont("Courier New", 18)
        self.clock = pygame.time.Clock()  # Fps variable

        self.x_mov = [False, False]  # Used to check left and right key detection
        self.y_mov = [False, False]  # Same but for the up and down

        self.colors = {"White": (255, 255, 255),
                       "Gray": (125, 125, 125)}

        self.debugMode = False


        # This dictionary is used to load images from data/images/
        self.assets = {
            'player': load_imgs("player/"),
            'wall': img_loader("tiles/wall.png"),
            'floor': img_loader("tiles/floor.png"),
            'corner': img_loader("tiles/corner.png"),
            'portal': img_loader("tiles/portal.png"),
            'bg': pygame.transform.scale(pygame.image.load('data/images/tiles/idea-bg_trophee-nsi.png').convert(), (1530, 1100))
        }

        self.portalWidth, self.portalHeight = self.assets['portal'].get_width(), self.assets['portal'].get_height()
        self.bg = self.assets['bg']


        # Player scrip
        self.player = player(self, 'player', (125, 50), 3)

        # Create the variables used for the camera
        self.camera = pygame.Rect(0, 0, self.display_width, self.display_height)
        self.camera_offset_x = -(self.player.playerPos[0] - self.display_width // 2)
        self.camera_offset_y = -(self.player.playerPos[1] - self.display_height // 2)
        self.camera_offset = [0, 0]

        # Creates rects that blocks the player off
        self.limitLeft = pygame.Rect(-220, -220, 5, 770)
        self.limitRight = pygame.Rect(750, -220, 5, 770)
        self.limitUp = pygame.Rect(-220, -220, 975, 5)
        self.limitDown = pygame.Rect(-220, 500, 1075, 5)

        self.collisionList = [self.limitLeft, self.limitRight, self.limitUp, self.limitDown]

    def run(self):

        while True:
            self.display.fill((0, 0, 0))
            self.display.blit(self.bg, (-500 + self.camera_offset[0], -400 + self.camera_offset[1]))
            # Dictionary of every rectangle and their text
            sportTeleporters = {

                "Gymnastics":   {"CollisionBox": pygame.Rect(-100, -100, self.portalWidth, self.portalHeight),
                                 "Description": {"Text": self.font.render("Gymnastics", False, self.colors["White"])}
                                },
                "Rowing":       {"CollisionBox": pygame.Rect(120, -100, self.portalWidth, self.portalHeight),
                                 "Description": {"Text": self.font.render("Rowing", False, self.colors["White"])}
                                },
                "Cycling":      {"CollisionBox": pygame.Rect(340, -100, self.portalWidth, self.portalHeight),
                                 "Description": {"Text": self.font.render("Cycling", False, self.colors["White"])}
                                },
                "Football":     {"CollisionBox": pygame.Rect(560, -100, self.portalWidth, self.portalHeight),
                                 "Description": {"Text": self.font.render("Football", False, self.colors["White"])}
                                },

                "Athletics":    {"CollisionBox": pygame.Rect(-100, 270, self.portalWidth, self.portalHeight),
                                 "Description": {"Text": self.font.render("Athletics", False, self.colors["White"])}
                                },
                "Hockey":       {"CollisionBox": pygame.Rect(120, 270, self.portalWidth, self.portalHeight),
                                 "Description": {"Text": self.font.render("Hockey", False, self.colors["White"])}
                                },
                "Sailing":      {"CollisionBox": pygame.Rect(340, 270, self.portalWidth, self.portalHeight),
                                 "Description": {"Text": self.font.render("Sailing", False, self.colors["White"])}
                                },
                "Swimming":     {"CollisionBox": pygame.Rect(560, 270, self.portalWidth, self.portalHeight),
                                 "Description": {"Text": self.font.render("Swimming", False, self.colors["White"])}
                                }
            }

            ###### ----------- COLLISIONS CHECKING ----------- ######

            for i in range(len(self.collisionList)):
                self.player.collisionCheck(self.collisionList[i], 10, "wall")

            ###### ------------------------------------------- ######

            ###### ----------- CAMERA UPADTES ----------- ######

            self.camera_offset_x = -(self.player.playerPos[0] + self.player.size[0] / 2 - self.display_width / 2)
            self.camera_offset_y = -(self.player.playerPos[1] + self.player.size[1] / 2 - self.display_height / 2)
            self.camera_offset = [self.camera_offset_x, self.camera_offset_y]

            ###### ------------------------------------- ######

            ###### ----------- DRAWING ONTO DISPLAY ----------- ######
            index = 0
            for sport, data in sportTeleporters.items():
                index += 1
                collision_box = data["CollisionBox"].move(self.camera_offset)
                self.display.blit(self.assets["portal"], (data["CollisionBox"].x + self.camera_offset_x, data["CollisionBox"].y + self.camera_offset_y))
                description_text = data["Description"]["Text"]

                # Puts the text in relative to the rectangle and its hitbox
                text_rect = description_text.get_rect()
                if index <= 4:
                    text_rect.midtop = (collision_box.midbottom[0], (collision_box.midbottom[1] + 20))
                else:
                    text_rect.midtop = (collision_box.midbottom[0], (collision_box.midbottom[1] - self.portalHeight - 40))

                # Just draws the rectangle and text
                if self.debugMode:
                    pygame.draw.rect(self.display, self.colors["Gray"], collision_box)

                self.display.blit(description_text, text_rect)

                if self.player.collisionCheck(data["CollisionBox"], 10):
                    openUI(promptMenu, sport)

            if self.debugMode:
                fpsText = self.font.render(f"FPS: {self.clock.get_fps():.0f}", False, self.colors["White"])
                playerPosText = self.font.render(f"Pos: {self.player.playerPos[0]:.0f}, {self.player.playerPos[1]:.0f}", False, self.colors["White"])
                cameraOffText = self.font.render(f"CamOffset: {self.camera_offset[0]:.0f}, {self.camera_offset[1]:.0f}", False, self.colors["White"])

                self.display.blit(fpsText, (15, 25))
                self.display.blit(playerPosText, (15, 45))
                self.display.blit(cameraOffText, (15, 65))

            ###### -------------------------------------------- ######

            ###### ----------- PLAYER UPDATES ----------- ######

            self.player.render(self.display)

            self.player.update(((self.x_mov[1] - self.x_mov[0]) * self.player.speed, (self.y_mov[1] - self.y_mov[0]) * self.player.speed))

            if self.debugMode:
                pygame.draw.rect(self.display, self.colors["White"], self.player.playerRect().move(self.camera_offset))
                pygame.draw.rect(self.display, self.colors["Gray"], self.limitLeft.move(self.camera_offset))
                pygame.draw.rect(self.display, self.colors["Gray"], self.limitRight.move(self.camera_offset))
                pygame.draw.rect(self.display, self.colors["Gray"], self.limitUp.move(self.camera_offset))
                pygame.draw.rect(self.display, self.colors["Gray"], self.limitDown.move(self.camera_offset))

            ###### -------------------------------------- ######

            ###### ----------- KEY PRESS EVENTS ----------- ######

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # When key pressed
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q or event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        self.x_mov[0] = True
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        self.x_mov[1] = True
                    if event.key == pygame.K_z or event.key == pygame.K_w or event.key == pygame.K_UP:
                        self.y_mov[0] = True
                    if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        self.y_mov[1] = True
                    if event.key == pygame.K_LSHIFT:
                        self.player.speed = 5

                    # Opens the custom command prompt (ccp)
                    if event.key == pygame.K_t:
                        self.debugMode = not self.debugMode

                # When key released
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_q or event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        self.x_mov[0] = False
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        self.x_mov[1] = False
                    if event.key == pygame.K_z or event.key == pygame.K_w or event.key == pygame.K_UP:
                        self.y_mov[0] = False
                    if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        self.y_mov[1] = False
                    if event.key == pygame.K_LSHIFT:
                        self.player.speed = 3

                ###### ---------------------------------------- ######

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.flip()
            self.clock.tick(60)


gameProgram().run()
