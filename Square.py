import pygame

class Square:
    def __init__(self, size, background_color):
        self.surface = pygame.Surface((size, size))
        self.size = size
        self.background_color = background_color
        pygame.draw.rect(self.surface, background_color, (0, 0, size, size))
        self.piece = None
        self.ghost = False

    def get_surface(self):
        return self.surface
    
    def set_piece(self, piece):
        self.piece = piece
        if piece != None:
            pygame.Surface.blit(self.surface, piece.get_surface(), (0, 0))
        else:
            pygame.draw.rect(self.surface, self.background_color, (0, 0, self.size, self.size))

    def remove_piece(self):
        self.piece = None
        self.clear_surface()

    def get_piece(self):
        return self.piece
    
    def add_ghost(self):
        assert self.piece == None, 'ghost - piece collision'
        pygame.draw.circle(self.surface, (128, 128, 128, 128), (self.size / 2, self.size / 2), self.size * 0.3)
        self.ghost = True
    
    def clear_surface(self):
        pygame.draw.rect(self.surface, self.background_color, (0, 0, self.size, self.size))
        self.ghost = False

    def is_ghost(self):
        return self.ghost