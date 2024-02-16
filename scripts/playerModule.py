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
        self.playerPos = list(pos)
        self.size = size
        self.vel = [0, 0]
        self.spdFac = self.game.spdFactor

    def playerRect(self):
        return pygame.Rect(self.playerPos[0], self.playerPos[1], self.size[0], self.size[1])

    def update(self, movement=(0, 0)):
        self.playerPos[0] += movement[0]
        self.playerPos[1] += movement[1]

    def render(self, surface):
        surface.blit(self.game.assets['player'], (self.playerPos[0] + self.game.camera_offset_x, self.playerPos[1] + self.game.camera_offset_y))

    def collisionCheck(self, collider: pygame.Rect, tolerance, collideType="normal"):

        """
        :param collider: pygame.Rect object
        :param tolerance: an int
        :param collideType: "Wall": Makes the player enable to through the collision.
                            "Normal": Check whenever the player's Rect is touching the collider
        :return: True if there is a collision between the collider and the player's collider. False otherwise.
        """
        playerCollisionBox = self.playerRect()
        if collideType == "normal":
            if pygame.Rect.colliderect(playerCollisionBox, collider):
                # DOWN
                if abs(collider.top - playerCollisionBox.bottom + self.spdFac) < tolerance:
                    self.update((0, -2 * self.spdFac))
                # UP
                if abs(collider.bottom - playerCollisionBox.top - self.spdFac) < tolerance:
                    self.update((0, 2 * self.spdFac))
                # RIGHT
                if abs(collider.left - playerCollisionBox.right + self.spdFac) < tolerance:
                    self.update((-2 * self.spdFac, 0))
                # LEFT
                if abs(collider.right - playerCollisionBox.left - self.spdFac) < tolerance:
                    self.update((2 * self.spdFac, 0))
                return True


        if collideType == "wall":
            if pygame.Rect.colliderect(playerCollisionBox, collider):
                # DOWN
                if abs(collider.top - playerCollisionBox.bottom + self.spdFac) < tolerance:
                    playerCollisionBox.bottom = collider.top
                # UP
                if abs(collider.bottom - playerCollisionBox.top - self.spdFac) < tolerance:
                    playerCollisionBox.top = collider.bottom
                # RIGHT
                if abs(collider.left - playerCollisionBox.right + self.spdFac) < tolerance:
                    playerCollisionBox.right = collider.left
                # LEFT
                if abs(collider.right - playerCollisionBox.left - self.spdFac) < tolerance:
                    playerCollisionBox.left = collider.right

        self.playerPos[0] = playerCollisionBox.x
        self.playerPos[1] = playerCollisionBox.y