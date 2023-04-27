import pygame
from Square import Square
from Piece import Piece

class Board:
    def __init__(self, square_size, background_colors, piece_colors):
        self.square_size = square_size
        self.array = [[None for x in range(8)] for y in range(8)]
        self.surface = pygame.Surface((square_size * 8, square_size * 8))
        self.turn = 0
        self.selected = None
        self.ghost_squares = []
        self.mode = 'default'
        self.pieces_remaining = [12, 12]
        self.game_over = False

        #adding squares to the board
        for y in range(0, 8):
            for x in range(0, 8):
                square = Square(square_size, background_colors[(x + y) % 2])
                self.array[y][x] = square
                

        #adding pieces to the board
        for y in range(3):
            for x in range(8):
                piece = Piece(square_size, square_size * 0.8, piece_colors[1], 1)
                if (x +  y) % 2 == 1:
                    self.array[y][x].set_piece(piece)
                else:
                    self.array[y][x].set_piece(None)

        for y in range(5, 8):
            for x in range(8):
                piece = Piece(square_size, square_size * 0.8, piece_colors[0], -1)
                if (x +  y) % 2 == 1:
                    self.array[y][x].set_piece(piece)
                else:
                    self.array[y][x].set_piece(None)

    def get_selected(self):
        return self.selected
            
    def get_mode(self):
        return self.mode
    
    def set_mode(self, new_mode):
        assert new_mode in ['default', 'something_selected', 'capturing'], 'invalid mode'
        self.mode = new_mode

    def get_turn(self):
        return self.turn
    
    def switch_turn(self):
        if self.turn == 0:
            self.turn = 1
        else:
            self.turn = 0
    
    def get_surface(self):
        return self.surface
    
    def clear_selections(self):
        if self.selected != None:
            self.selected.deselect()
        self.selected = None
        for square in self.ghost_squares:
            square.clear_surface()
        self.ghost_squares = []
    
    def select(self, x, y, only_captures_flag = False):
        self.clear_selections()
        piece = self.array[y][x].get_piece()
        assert piece != None, 'cannot select a non-existent piece'
        piece.select()
        self.selected = piece
        
        if not only_captures_flag:
            considered_ghost_squares = self.valid_moves(x, y) + self.valid_captures(x, y)
        else:
            considered_ghost_squares = self.valid_captures(x, y)

        for chords in considered_ghost_squares:
            square = self.array[chords[1]][chords[0]]
            square.add_ghost()
            self.ghost_squares.append(square)


    def update(self):
        for y in range(len(self.array)):
            for x in range(len(self.array[0])):
                square = self.array[y][x]
                if square.get_piece() != None:
                    square.get_surface().blit(square.get_piece().get_surface(), (0, 0))
                pygame.Surface.blit(self.surface, square.get_surface(), (x * self.square_size, y * self.square_size))


    #returns true if a piece was catprued, otherwise returns false
    def move_piece(self, starting_x, starting_y, ending_x, ending_y):
        assert self.array[starting_y][starting_x].get_piece() != None, f'starting coords ({starting_x}, {starting_y}) do not contain a piece'
        assert self.array[ending_y][ending_x].get_piece() == None, f'ending coords ({ending_x}, {ending_y}) already contain a piece'

        starting_square = self.array[starting_y][starting_x]
        piece = starting_square.get_piece()
        ending_square = self.array[ending_y][ending_x]

        starting_square.set_piece(None)
        ending_square.set_piece(piece)

        self.clear_selections()

        #promote pieces if they reach the end
        if (piece.move_direction == 1 and ending_y == 7) or (piece.move_direction == -1 and ending_y == 0):
            piece.promote()

        #remove captured pieces and update the remaining count
        if abs(starting_x - ending_x) == 2:
            x = (starting_x + ending_x) // 2
            y = (starting_y + ending_y) // 2
            square = self.array[y][x]
            captured_piece = square.get_piece()
            
            if captured_piece.get_team() == 0:
                self.pieces_remaining[0] -= 1
            elif captured_piece.get_team() == 1:
                self.pieces_remaining[1] -= 1

            if min(self.pieces_remaining) == 0:
                self.game_over = True

            self.array[y][x].remove_piece()
            
            return True
        else:
            return False

    
    def valid_moves(self, x, y):
        moves = []
        piece = self.array[y][x].get_piece()
        for x_shift in range(-1, 2, 2):
            potential_chords = (x + x_shift, y + piece.move_direction)
            if 0 <= potential_chords[0] < 8 and 0 <= potential_chords[1] < 8 and self.array[potential_chords[1]][potential_chords[0]].get_piece() == None:
                moves.append(potential_chords)

        if piece.is_royal:
            for x_shift in range(-1, 2, 2):
                potential_chords = (x + x_shift, y + piece.move_direction * -1)
                if 0 <= potential_chords[0] < 8 and 0 <= potential_chords[1] < 8 and self.array[potential_chords[1]][potential_chords[0]].get_piece() == None:
                    moves.append(potential_chords)

        return moves
    

    def valid_captures(self, x, y):
        moves = []
        piece = self.array[y][x].get_piece()
        for x_shift in range(-1, 2, 2):
            potential_chords = (x + x_shift * 2, y + piece.move_direction * 2)
            opponent_chords = (x + x_shift, y + piece.move_direction)
            if 0 <= potential_chords[0] < 8 and 0 <= potential_chords[1] < 8 and self.array[potential_chords[1]][potential_chords[0]].get_piece() == None and self.array[opponent_chords[1]][opponent_chords[0]].get_piece() != None and self.array[opponent_chords[1]][opponent_chords[0]].get_piece().opposes(piece):
                moves.append(potential_chords)

        if piece.is_royal:
            for x_shift in range(-1, 2, 2):
                potential_chords = (x + x_shift * 2, y + piece.move_direction * -2)
                opponent_chords = (x + x_shift, y + piece.move_direction * -1)
                if 0 <= potential_chords[0] < 8 and 0 <= potential_chords[1] < 8 and self.array[potential_chords[1]][potential_chords[0]].get_piece() == None and self.array[opponent_chords[1]][opponent_chords[0]].get_piece() != None and self.array[opponent_chords[1]][opponent_chords[0]].get_piece().opposes(piece):
                    moves.append(potential_chords)

        return moves
    

    #find the chords of a piece on the board
    def find_piece(self, piece):
        for y in range(len(self.array)):
            for x in range(len(self.array[0])):
                if self.array[y][x].get_piece() == piece:
                    return (x, y)
                
        return False
    
    

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((400, 400))
    board = Board(50, ((0, 0, 0), (255, 255, 255)), ((255, 0, 0), (0, 0, 255)))

    board.array[3][0].add_ghost()    
    
    board.update()
    pygame.Surface.blit(screen, board.get_surface(), (0, 0))
    pygame.display.flip()

    

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False

        


    

