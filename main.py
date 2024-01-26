"""
File Created By BERGE Liam & REEVES Guillaume
Graphics Made by Vix (SCARPA Ayden)
Created on 2023-12-04
Last Updated on 2024-01-25
"""
import sys
import pygame
from scripts.playerModule import player
from scripts.utility import img_loader
from scripts.UIsModule import openUI, cMenu, promptMenu, ResultsDisplayer

pygame.init()

class gameProgram:
    def __init__(self):
        # Initialises the pygame basic window configs
        pygame.display.set_caption("Trophy NSI")

        self.ratio_Factor = 2
        self.screen_width, self.screen_height = 600, 600
        self.display_width = self.screen_width / self.ratio_Factor
        self.display_height = self.screen_height / self.ratio_Factor

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.display = pygame.Surface((self.display_width, self.display_height))

        self.font = pygame.font.SysFont("Courier New", 18)
        self.clock = pygame.time.Clock()  # Fps variable
        self.camera = pygame.Rect(0, 0, self.display_width, self.display_height)

        self.x_mov = [False, False]  # Used to check left and right key detection
        self.y_mov = [False, False]  # Same but for the up and down

        self.colors = {"White": (255, 255, 255),
                       "Gray": (125, 125, 125)}

        self.debugMode = False

        # You can see the code for it in the playerModule.py file
        self.player_SpeedFactor = 2
        self.player = player(self, 'player', (138, 130), (28, 30))
        self.playerRect = pygame.Rect(self.player.entity_pos[0] + 9, self.player.entity_pos[1],
                                      self.player.size[0] - 10, self.player.size[1])
        self.assets = {
            'player': img_loader('entities/player/playerImg.png'),
        }

        self.camera_offset_x = -(self.player.entity_pos[0] - self.display_width / 2)
        self.camera_offset_y = -(self.player.entity_pos[1] - self.display_height / 2)

        self.limitLeft = pygame.Rect(-245, 0, 5, self.display_height)
        self.limitRight = pygame.Rect(self.display_width + 240, 0, 5, self.display_height)
        self.limitUp = pygame.Rect(-245, 0, self.display_width + 490, 5)
        self.limitDown = pygame.Rect(-245, self.display_height - 5, self.display_width + 490, 5)

        self.collisionList = [self.limitLeft, self.limitRight, self.limitUp, self.limitDown]

    def run(self):

        while True:
            # Dictionary of every rectangle and their text
            sportTeleporters = {
                "Rowing": {"CollisionBox": pygame.Rect(-170, 230, 30, 30),
                           "Description": {"Text": self.font.render("Rowing", False, self.colors["White"]),
                                           "Pos": [-187 + self.camera_offset_x, 270 + self.camera_offset_y]}
                           },
                "Hockey": {"CollisionBox": pygame.Rect(-75, 230, 30, 30),
                           "Description": {"Text": self.font.render("Hockey", False, self.colors["White"]),
                                           "Pos": [-90 + self.camera_offset_x, 270 + self.camera_offset_y]}
                           },
                "Gymnastics": {"CollisionBox": pygame.Rect(30, 230, 30, 30),
                               "Description": {"Text": self.font.render("Gymnastics", False, self.colors["White"]),
                                               "Pos": [-7 + self.camera_offset_x, 270 + self.camera_offset_y]}
                               },
                "Athletics": {"CollisionBox": pygame.Rect(150, 230, 30, 30),
                              "Description": {"Text": self.font.render("Athletics", False, self.colors["White"]),
                                              "Pos": [117 + self.camera_offset_x, 270 + self.camera_offset_y]}
                              },
                "Cycling": {"CollisionBox": pygame.Rect(250, 230, 30, 30),
                            "Description": {"Text": self.font.render("Cycling", False, self.colors["White"]),
                                            "Pos": [220 + self.camera_offset_x, 270 + self.camera_offset_y]}
                            },
                "Football": {"CollisionBox": pygame.Rect(340, 230, 30, 30),
                             "Description": {"Text": self.font.render("Football", False, self.colors["White"]),
                                             "Pos": [307 + self.camera_offset_x, 270 + self.camera_offset_y]}
                             },
                "Sailing": {"CollisionBox": pygame.Rect(430, 230, 30, 30),
                            "Description": {"Text": self.font.render("Sailing", False, self.colors["White"]),
                                            "Pos": [387 + self.camera_offset_x, 270 + self.camera_offset_y]}
                            },
                "Swimming": {"CollisionBox": pygame.Rect(230, 70, 30, 30),
                             "Description": {"Text": self.font.render("Swimming", False, self.colors["White"]),
                                             "Pos": [197 + self.camera_offset_x, 25 + self.camera_offset_y]}
                             }
            }

            self.display.fill((30, 30, 30))  # Renders the screen black


            ###### ----------- COLLISIONS CHECKING ----------- ######

            for i in range(len(self.collisionList)):
                self.player.collisionCheck(self.collisionList[i], 10, "wall")

            ###### ------------------------------------------- ######

            ###### ----------- CAMERA UPADTES ----------- ######

            self.camera_offset_x = -(self.player.entity_pos[0] + 12 - self.display_width / 2)
            self.camera_offset_y = -(self.player.entity_pos[1] + 20 - self.display_height / 2)
            self.camera.topleft = (self.camera_offset_x, self.camera_offset_y)

            ###### ------------------------------------- ######

            ###### ----------- DRAWING ONTO DISPLAY ----------- ######

            for sport, data in sportTeleporters.items():
                collision_box = data["CollisionBox"].move(self.camera.topleft)
                description_text = data["Description"]["Text"]

                # Puts the text in relative to the rectangle and its hitbox
                text_rect = description_text.get_rect()
                text_rect.midtop = collision_box.midbottom

                # Just draws the rectangle and text
                pygame.draw.rect(self.display, self.colors["Gray"], collision_box)
                self.display.blit(description_text, text_rect)

                if self.player.collisionCheck(data["CollisionBox"], 10, "wall"):
                    openUI(promptMenu, sport)

            if self.debugMode:
                fpsText = self.font.render(f"FPS: {self.clock.get_fps():.0f}", False, self.colors["White"])
                self.display.blit(fpsText, (15, 25))

                playerPosText = self.font.render(
                    f"Pos: {self.player.entity_pos[0]:.0f}, {self.player.entity_pos[1]:.0f}", False,
                    self.colors["White"])
                self.display.blit(playerPosText, (15, 45))

            ###### -------------------------------------------- ######

            ###### ----------- PLAYER UPDATES ----------- ######

            if self.debugMode:
                pygame.draw.rect(self.display, self.colors["Gray"], self.playerRect.move(self.camera.topleft))
            self.player.render(self.display)
            self.player.update(((self.x_mov[1] - self.x_mov[0]) * self.player_SpeedFactor, 0))
            self.player.update((0, (self.y_mov[1] - self.y_mov[0]) * self.player_SpeedFactor))
            self.playerRect = pygame.Rect(self.player.entity_pos[0] + 9, self.player.entity_pos[1],
                                          self.player.size[0] - 10, self.player.size[1])

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

                    # Opens the custom command prompt (ccp)
                    if event.key == pygame.K_t:
                        text = str(openUI(cMenu))
                        if text != "":
                            args, parameters = text.split(), []
                            c = args.pop(0)
                            c = c.lower()
                            parameters.extend(args)
                            if parameters:
                                if c == "tp" or c == "teleport":
                                    self.player.entity_pos = [float(parameters[0]), float(parameters[1])]
                                elif c == "debug" or c == "debugger" or c == "db":
                                    if parameters[0] == "True":
                                        self.debugMode = True
                                    elif parameters[0] == "False":
                                        self.debugMode = False
                            else:
                                print(f"No Value Provided to {c}")

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

                ###### ---------------------------------------- ######

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)


gameProgram().run()
