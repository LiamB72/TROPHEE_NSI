"""
File Created By BERGE Liam
Created on 2023-12-05
Last Update on 2024-01-25
"""
import pygame


class player:
    def __init__(self, game, entity_type, pos, size):

        self.game = game
        self.type = entity_type
        self.entity_pos = list(pos)
        self.size = size
        self.vel = [0, 0]
        self.spdFac = self.game.player_SpeedFactor

    def update(self, movement=(0, 0)):
        frame_movement = (movement[0] + self.vel[0], movement[1] + self.vel[1])
        self.entity_pos[0] += frame_movement[0]
        self.entity_pos[1] += frame_movement[1]

    def render(self, surface):
        surface.blit(self.game.assets['player'], (self.entity_pos[0] + self.game.camera_offset_x, self.entity_pos[1] + self.game.camera_offset_y))

    def collisionCheck(self, collider: pygame.Rect, tolerance, collideType="normal"):

        """
        :param collider: pygame.Rect object
        :param tolerance: an int
        :param collideType: "wall" : Makes the player enable to thru the collision.
                            "normal" : Just check whenever the player's Rect is touching the collider
        :return: True if there is a collision between the collider and the player's collider. False otherwise.
        """

        if collideType == "normal":
            if pygame.Rect.colliderect(self.game.playerRect, collider):
                return True
            return False


        if collideType == "wall":
            if pygame.Rect.colliderect(self.game.playerRect, collider):
                # DOWN
                if abs(collider.top - self.game.playerRect.bottom + self.spdFac) < tolerance:
                    self.update((0, -2 * self.spdFac))
                # UP
                if abs(collider.bottom - self.game.playerRect.top - self.spdFac) < tolerance:
                    self.update((0, 2 * self.spdFac))
                # RIGHT
                if abs(collider.left - self.game.playerRect.right + self.spdFac) < tolerance:
                    self.update((-2 * self.spdFac, 0))
                # LEFT
                if abs(collider.right - self.game.playerRect.left - self.spdFac) < tolerance:
                    self.update((2 * self.spdFac, 0))

                return True