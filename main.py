#Berge Liam -> Coder
#Reeves Guillaume -> Coder
#Vix -> designer

import sys

import pygame

from scripts.playerModule import player
from scripts.utility import img_loader
from scripts.UIsModule import openUI, cMenu

pygame.init()


class gameProgram:
    def __init__(self):
        # Initialises the pygame basic window configs
        pygame.display.set_caption("Trophy NSI")
        self.ratio_Factor = 2
        self.screen_width, self.screen_height = 600, 600
        self.display_width, self.display_height = self.screen_width / self.ratio_Factor, self.screen_height / self.ratio_Factor
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.display = pygame.Surface((self.display_width, self.display_height))
        self.font = pygame.font.SysFont("Courier New", 18)
        self.camera = pygame.Rect(0, 0, self.display_width, self.display_height)
        self.clock = pygame.time.Clock()  # Fps variable

        self.x_mov = [False, False]  # Used to check left and right key detection
        self.y_mov = [False, False]  # Same but for the up and down

        # You can see the code for it in the playerModule.py file
        self.player_SpeedFactor = 1.2
        self.player = player(self, 'player', ((self.display_width/2),(self.display_height/2)), (28, 30))
        self.playerRect = pygame.Rect(self.player.entity_pos[0] + 9, self.player.entity_pos[1],
                                      self.player.size[0] - 10, self.player.size[1])
        self.assets = {
            'player': img_loader('entities/player/playerImg.png'),
        }

        self.camera_offset_x = -(self.player.entity_pos[0] - self.display_width / 2)
        self.camera_offset_y = -(self.player.entity_pos[1] - self.display_height / 2)

        self.limitLeft = pygame.Rect(0, 0, 5, self.display_height)
        self.limitRight = pygame.Rect(self.display_width-5, 0, 5, self.display_height)
        self.limitUp = pygame.Rect(0, 0, self.display_width, 5)
        self.limitDown = pygame.Rect(0, self.display_height-5, self.display_width, 5)
        self.rectFootball = pygame.Rect(150, 25, 60, 35)

        self.teleLocations = {"Lobby": [self.display_width/2, self.display_height/2],
                              "football": [-15, 0]}
        self.teleported = False


    def run(self):

        while True:

            self.display.fill((30, 30, 30))  # Renders the screen black

            # Creates&Updates the rect of the player's, basically it's collision/bonding box.

            # Collision Checking HERE
            if self.player.collisionCheck(self.rectFootball, 10):
                self.player.entity_pos = self.teleLocations["football"]
            self.player.collisionCheck(self.limitLeft, 10, "wall")
            self.player.collisionCheck(self.limitRight, 10, "wall")
            self.player.collisionCheck(self.limitUp, 10, "wall")
            self.player.collisionCheck(self.limitDown, 10, "wall")

            self.camera_offset_x = -(self.player.entity_pos[0] + 12 - self.display_width / 2)
            self.camera_offset_y = -(self.player.entity_pos[1] + 20 - self.display_height / 2)
            self.camera.topleft = (self.camera_offset_x, self.camera_offset_y)

            # !! Draw rects here !!
            pygame.draw.rect(self.display, (125, 125, 125), self.rectFootball.move(self.camera.topleft))
            pygame.draw.rect(self.display, (125, 125, 125), self.limitLeft.move(self.camera.topleft))
            pygame.draw.rect(self.display, (125, 125, 125), self.limitRight.move(self.camera.topleft))
            pygame.draw.rect(self.display, (125, 125, 125), self.limitUp.move(self.camera.topleft))
            pygame.draw.rect(self.display, (125, 125, 125), self.limitDown.move(self.camera.topleft))

            # See code in playerModule.py
            #pygame.draw.rect(self.display, (125, 255, 125), self.playerRect.move(self.camera.topleft))
            self.player.render(self.display)
            self.player.update(((self.x_mov[1] - self.x_mov[0]) * self.player_SpeedFactor, 0))
            self.player.update((0, (self.y_mov[1] - self.y_mov[0]) * self.player_SpeedFactor))
            self.playerRect = pygame.Rect(self.player.entity_pos[0] + 9, self.player.entity_pos[1], self.player.size[0] - 10, self.player.size[1])

            # if self.player.collisionCheck(self.tpBackCollision, 10):
            #     self.player.entity_pos = self.ballSport["football"]
            #     self.teleported = True

            # Shows the current fps & the player's position
            fpsText = self.font.render(f"fps: {self.clock.get_fps():.0f}",
                                       False,
                                       (255, 255, 255))

            playerPosText = self.font.render(f"Pos: {self.player.entity_pos[0]:.0f}, {self.player.entity_pos[1]:.0f}",
                                             False,
                                             (255, 255, 255))

            self.display.blit(fpsText, (15, 25))
            self.display.blit(playerPosText, (15, 45))

            # Makes the display on a bigger scale due to pixel art.
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

                    if event.key == pygame.K_t:
                        text = str(openUI(cMenu))
                        args, parameters = text.split(), []
                        c = args.pop(0)
                        parameters.extend(args)
                        if c == "tp" or c == "teleportPlayer" or c == "teleport":
                            self.player.entity_pos = [float(parameters[0]), float(parameters[1])]

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

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()

            # Obviously.
            self.clock.tick(60)

gameProgram().run()
