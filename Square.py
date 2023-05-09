import pygame

class Square:
    def __init__(self, size, background_color, ghost_square_color):
        self.surface = pygame.Surface((size, size))
        self.size = size
        self.background_color = background_color
        pygame.draw.rect(self.surface, background_color, (0, 0, size, size))
        self.piece = None
        self.ghost = False
        self.ghost_square_color = ghost_square_color

    def get_surface(self):
        return self.surface
    
    def set_surface(self, new_surface):
        assert type(new_surface) == pygame.Surface, f'invalid surface arg {new_surface}'
        self.surface = new_surface
    
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
        pygame.draw.circle(self.surface, self.ghost_square_color, (self.size / 2, self.size / 2), self.size * 0.3)
        self.ghost = True
    
    def clear_surface(self):
        pygame.draw.rect(self.surface, self.background_color, (0, 0, self.size, self.size))
        self.ghost = False

    def is_ghost(self):
        return self.ghost
    
    def copy(self):
        copy = Square(self.size, self.background_color, self.ghost_square_color)        
        if self.piece != None:
            copy.piece = self.piece.copy()

        return copy