import pygame

class entityPhysics:
    def __init__(self, game, entity_type, pos, size):
        
        self.game = game
        self.type = entity_type
        self.entity_pos = list(pos)
        self.size = size
        self.vel = [0, 0]
        
    def update(self, movement=(0, 0)):        
        frame_movement = (movement[0] + self.vel[0], movement[1] + self.vel[1])
        
        self.entity_pos[0] += frame_movement[0]
        self.entity_pos[1] += frame_movement[1]
        
    def render(self, surface):
        surface.blit(self.game.assets['player'], self.entity_pos)