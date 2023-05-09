import pygame

class Piece:
    def __init__(self, background_size, diameter, color, move_direction, inner_color):
        self.background_size = background_size
        self.diameter = diameter
        self.color = color
        self.move_direction = move_direction
        self.inner_color = inner_color
        
        self.surface = pygame.Surface((background_size, background_size))
        self.surface.set_colorkey((0, 0, 0))
        self.is_royal = False
        self.reset_surface()
        
        if self.move_direction == -1:
            self.team = 0
        else:
            self.team = 1


    def get_surface(self):
        return self.surface
    
    def set_surface(self, new_surface):
        assert type(new_surface) == pygame.Surface, f'invalid surface arg {new_surface}'
        self.surface = new_surface
    
    def reset_surface(self):
        pygame.draw.circle(self.surface, self.color, (self.background_size / 2, self.background_size / 2), self.diameter / 2) #outer circle
        pygame.draw.circle(self.surface, self.inner_color, (self.background_size / 2, self.background_size / 2), self.diameter * 0.8 / 2) #inner circle
        pygame.draw.circle(self.surface, self.inner_color, (self.background_size / 2, self.background_size / 2), self.diameter / 2, 1) #border

        if self.is_royal:
            pygame.draw.circle(self.surface, (1, 1, 1), (self.background_size / 2, self.background_size / 2), self.diameter / 4, 4) #small circle for royal
    
    def select(self):
        pygame.draw.circle(self.surface, (168, 142, 25), (self.background_size / 2, self.background_size / 2), self.diameter / 2, 3) #gold

    def deselect(self):
        self.reset_surface()

    def opposes(self, other_piece):
        return self.team != other_piece.team
    
    def promote(self):
        pygame.draw.circle(self.surface, (1, 1, 1), (self.background_size / 2, self.background_size / 2), self.diameter / 4, 4)
        self.is_royal = True

    def get_team(self):
        return self.team
    
    def copy(self):
        copy = Piece(self.background_size, self.diameter, self.color, self.move_direction, self.inner_color)
        copy.set_surface(self.surface.copy())

        return copy
    
        


