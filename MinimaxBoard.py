from Board import Board
from copy import deepcopy

class MinimaxBoard(Board):

    def copy(self):
        copy = MinimaxBoard(self.square_size, self.background_colors, self.piece_colors, self.inner_piece_colors, self.ghost_square_color)
        copy.set_surface(self.surface.copy())
        copy.array = [[square.copy() for square in row] for row in self.array]
        copy.turn = self.turn
        
        return copy
    
    

    def possible_moves(self):
        moves = []
        for y in range(len(self.array)):
            for x in range(len(self.array[0])):
                piece = self.array[y][x].get_piece()
                if piece != None and piece.get_team() == self.turn:
                    for move in self.valid_moves(x, y) + self.valid_captures(x, y):
                        moves.append((x, y, move[0], move[1]))

        return moves


    def piece_value_eval(self):
        p0_score = 0
        p1_score = 0

        for row in self.array:
            for square in row:
                piece = square.get_piece()
                if piece != None:
                    if piece.get_team() == 0 and not piece.is_royal:
                        p0_score += 1
                    elif piece.get_team() == 0 and piece.is_royal:
                        p0_score += 2
                    elif piece.get_team() == 1 and not piece.is_royal:
                        p1_score += 1
                    elif piece.get_team() == 1 and piece.is_royal:
                        p1_score += 2
        return p0_score - p1_score
    

    def piece_placement_eval(self):
        p0_score = 0
        p1_score = 0

        for y in range(len(self.array)):
            for x in range(len(self.array[0])):
                piece = self.array[y][x].get_piece()
                if piece != None:
                    if piece.move_direction == -1 and not piece.is_royal:
                        p0_score += 5 + 8 - y
                    elif piece.move_direction == -1 and piece.is_royal:
                        p0_score += 15
                    elif piece.move_direction == 1 and not piece.is_royal:
                        p1_score += 5 + y
                    elif piece.move_direction == 1 and piece.is_royal:
                        p1_score += 15

        return p0_score - p1_score
    

    def more_royals(self):
        #returns None if they have the same number of royals
        p0_score = 0
        p1_score = 1

        for row in self.array:
            for square in row:
                piece = square.get_piece()
                if piece != None and piece.is_royal:
                    if piece.get_team() == 0:
                        p0_score += 1
                    elif piece.get_team() == 1:
                        p1_score += 1
        
        if p0_score > p1_score:
            return 0
        elif p1_score > p0_score:
            return 1
        else:
            return None
        

if __name__ == '__main__':
    import pygame
    pygame.init()
    screen = pygame.display.set_mode((400, 400))
    board = MinimaxBoard(50, ((0, 0, 0), (255, 255, 255)), ((255, 0, 0), (0, 0, 255)), ((50, 50, 50), (200, 200, 200)), (153, 122, 75))

    
    board.update()
    pygame.Surface.blit(screen, board.get_surface(), (0, 0))
    pygame.display.flip()

    print(board.possible_moves())

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
        
                    
