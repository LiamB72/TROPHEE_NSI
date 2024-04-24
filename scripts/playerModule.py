"""
File Created By BERGE Liam
Created on 2023-12-05
Last Update on 2024-01-25
"""
import pygame


class player:
    def __init__(self, game, entity_type, pos, spdFactor=1):

        self.game = game
        self.type = entity_type
        self.playerPos = list(pos)
        self.speed = spdFactor
        self.state = 0
        self.size = [self.game.assets['player'][self.state].get_width(), self.game.assets['player'][self.state].get_height()]

    def playerRect(self):
        return pygame.Rect(self.playerPos[0], self.playerPos[1], self.size[0], self.size[1])

    def update(self, movement=(0, 0)):
        dx, dy = movement
        self.playerPos[0] += dx
        self.playerPos[1] += dy

        if dx > 0:
            self.state = 2
        elif dx < 0:
            self.state = 1
        elif dy > 0:
            self.state = 4
        elif dy < 0:
            self.state = 3
        else:
            self.state = 0

    def render(self, surface):
        surface.blit(self.game.assets['player'][self.state],
                         (self.playerPos[0] + self.game.camera_offset_x, self.playerPos[1] + self.game.camera_offset_y))

    def collisionCheck(self, collider: pygame.Rect, tolerance, collideType="normal"):

        """
        :param collider: pygame.Rect object
        :param tolerance: an int
        :param collideType: "Wall": Makes the player enable to through the collision.
                            "Normal": Check whenever the player's Rect is touching the collider
        :return: True if there is a collision between the collider and the player's collider. False otherwise.
        """
        playerCollisionBox = self.playerRect()
        if pygame.Rect.colliderect(playerCollisionBox, collider):
            if collideType == "normal":
                if abs(collider.top - playerCollisionBox.bottom + self.speed) < tolerance:
                    self.update((0, -2 * self.speed))
                if abs(collider.bottom - playerCollisionBox.top - self.speed) < tolerance:
                    self.update((0, 2 * self.speed))
                if abs(collider.left - playerCollisionBox.right + self.speed) < tolerance:
                    self.update((-2 * self.speed, 0))
                if abs(collider.right - playerCollisionBox.left - self.speed) < tolerance:
                    self.update((2 * self.speed, 0))
                return True

            if collideType == "wall":
                if abs(collider.top - playerCollisionBox.bottom + self.speed) < tolerance:
                    playerCollisionBox.bottom = collider.top
                if abs(collider.bottom - playerCollisionBox.top - self.speed) < tolerance:
                    playerCollisionBox.top = collider.bottom
                if abs(collider.left - playerCollisionBox.right + self.speed) < tolerance:
                    playerCollisionBox.right = collider.left
                if abs(collider.right - playerCollisionBox.left - self.speed) < tolerance:
                    playerCollisionBox.left = collider.right

            self.playerPos[0] = playerCollisionBox.x
            self.playerPos[1] = playerCollisionBox.y