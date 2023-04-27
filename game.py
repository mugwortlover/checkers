import pygame
import math
from Board import Board

#global constants
SQUARE_SIZE = 75

#global vars
board = Board(SQUARE_SIZE, ((0, 0, 0), (255, 255, 255)), ((255, 0, 0), (0, 0, 255)))


def handle_clicks(x, y):
    mode = board.get_mode()
    turn = board.get_turn()
    square_clicked = board.array[y][x]
    piece_clicked = square_clicked.get_piece()

    if board.game_over:
        return

    if mode == 'default':
        #if the user clicked on a piece and its the right team, select that piece
        if piece_clicked != None and piece_clicked.get_team() == turn:
            board.select(x, y)

            #change the mode to something_selected
            board.set_mode('something_selected')

    elif mode == 'something_selected':
        #if the user clicked on a ghost square, move to that square, clear
        if square_clicked.is_ghost():
            selected = board.get_selected()
            selected_chords = board.find_piece(selected)
            capture = board.move_piece(selected_chords[0], selected_chords[1], x, y)
            board.set_mode('default')

            #if it was a capture and the piece can capture again:
                #select the piece again and add the right ghost squares (only for captures)
                #change mode to capturing
            #otherwise, switch turn

            if capture and board.valid_captures(x, y) != []:
                board.select(x, y, only_captures_flag = True)
                board.set_mode('capturing')
            else:
                board.switch_turn()

            
        #if the user clicked on something other than a ghost square, clear, change mode to default
        else:
            #if the user clicked on another piece of the same team
            if piece_clicked != None and piece_clicked.get_team() == turn:
                board.select(x, y)
            
            else: 
                board.clear_selections()
                board.set_mode('default')

    elif mode == 'capturing':
        #if the user clicked on a ghost square:
            #move the piece to that square, clear
            #if the piece can capture again:
                #select the piece again and add the right ghost squares (only for captures)
            #otherwise, switch turn, change mode to default

        if square_clicked.is_ghost():
            selected = board.get_selected()
            selected_chords = board.find_piece(selected)
            capture = board.move_piece(selected_chords[0], selected_chords[1], x, y)
            if board.valid_captures(x, y) != []:
                board.select(x, y, only_captures_flag = True)
            else:
                board.switch_turn()
                board.set_mode('default')

        

def main():
    pygame.init()
    screen = pygame.display.set_mode((SQUARE_SIZE * 8, SQUARE_SIZE * 8))
    pygame.display.set_caption('Checkers')
    mouse_down_last = False



    running = True
    while running:
        #check to see if the user has quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #if the user just clicked on something, handle it
        mouse_down = pygame.mouse.get_pressed()[0]
        if mouse_down and not mouse_down_last:
            pos = pygame.mouse.get_pos()
            x, y = math.floor(pos[0] / SQUARE_SIZE), math.floor(pos[1] / SQUARE_SIZE)
            handle_clicks(x, y)
        mouse_down_last = mouse_down

        screen.fill((255, 255, 255))
        
        board.update()
        screen.blit(board.get_surface(), (0, 0))

        pygame.display.flip()


    pygame.quit()


if __name__ == '__main__':
    main()