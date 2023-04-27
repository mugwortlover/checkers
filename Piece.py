import pygame

class Piece:
    def __init__(self, background_size, diameter, color, move_direction):
        self.color = color
        self.diameter = diameter
        self.background_size = background_size
        self.surface = pygame.Surface((background_size, background_size))
        self.surface.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.surface, color, (background_size / 2, background_size / 2), diameter / 2)
        self.is_royal = False
        self.move_direction = move_direction
        
        if self.move_direction == -1:
            self.team = 0
        else:
            self.team = 1

    def get_surface(self):
        return self.surface
    
    def select(self):
        pygame.draw.circle(self.surface, (168, 142, 25), (self.background_size / 2, self.background_size / 2), self.diameter / 2, 3)

    def deselect(self):
        pygame.draw.circle(self.surface, self.color, (self.background_size / 2, self.background_size / 2), self.diameter / 2, 3)

    def opposes(self, other_piece):
        return self.team != other_piece.team
    
    def promote(self):
        pygame.draw.circle(self.surface, (1, 1, 1), (self.background_size / 2, self.background_size / 2), self.diameter / 4, 4)
        self.is_royal = True

    def get_team(self):
        return self.team
    
        


