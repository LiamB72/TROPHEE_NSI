class tilemap:
    def __init__(self, game, tile_size=16):
        self.tile_size = tile_size
        self.tileMap = {}
        self.offgrid_tiles = []
        
        for i in range(10):
            self.tileMap[str(3 + i) + ';10'] = {"type": "grass", "variant": 1, "pos": (3 + i, 10)}
            self.tileMap['10;' + str(5 + i)] = {"type": "stone", "variant": 1, "pos": (10, 5 + i)}
            
    def render(self, surf):
        for location in self.tileMap:
            tile = self.tileMap[location]
            surf.blit(self.game.assets[tile['type']][tile['variant']][tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size])