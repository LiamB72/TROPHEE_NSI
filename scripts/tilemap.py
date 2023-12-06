import pygame

LOOKOUT_OFFSET = [(-1,-1), (0,-1), (1,-1),
                  (-1, 0), (0,0), (1,0),
                  (-1,1), (0,1), (1,1)]

TILES_COLLISION = {'stone'} # Dictionary is used, so it's more efficient and avoid duplicates when searching thru.

class tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tileMap = {}
        self.decor_tiles = []

        #Generating tiles
        for i in range(10):
            self.tileMap[str(3 + i) + ';10'] = {"type": "grass", "variant": 1, "pos": (3 + i, 10)}
            self.tileMap['10;' + str(5 + i)] = {"type": "stone", "variant": 1, "pos": (10, 5 + i)}

    def tiles_lookout(self, player_pos):
        tiles_found = [] # List that will be returned

        # A tuple of the position of the tile depending on the player's position, altogether, in an int
        # so no float number can bug the system.
        tile_location = (int(player_pos[0] // self.tile_size), int(player_pos[1] // self.tile_size))

        for offset in LOOKOUT_OFFSET:
            check_location = str(tile_location[0] + offset[0]) + ";" + str(tile_location[1] + offset[1])

            if check_location in self.tileMap:
                tiles_found.append(self.tileMap[check_location])

        return tiles_found

    def collision_detection(self, player_pos):
        collision_list = []

        for tile in self.tiles_lookout(player_pos):
            if tile['type'] in TILES_COLLISION:

                collision_list.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size), self.tile_size, self.tile_size)

        return collision_list
    def render(self, surface):
        for tile in self.decor_tiles:

            surface.blit(self.game.assets[tile['type']][tile['variant']], tile['pos'])

        for location in self.tileMap:

            tile = self.tileMap[location]
            surface.blit(self.game.assets[tile['type']][tile['variant']][tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size])