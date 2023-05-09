from MinimaxBoard import MinimaxBoard
from Tree import Tree, Node
from Piece import Piece
from copy import copy


def print_board(board):
    array = board.array
    txt = ''
    for row in array:
        row_txt = ''
        for item in row:
            piece = item.get_piece()
            if type(piece) == Piece:
                row_txt += str(piece.get_team()) + ' '
            elif piece == None:
                row_txt += '_ '
        txt += row_txt + '\n'
    print(txt)


def minimax(board, depth):
    starting = board.copy()
    tree = Tree(starting)
    
    def create_children(node):
        parent_board = node.get_data()
        for move in parent_board.possible_moves():
            board = parent_board.copy()
            board.move_piece(move[0], move[1], move[2], move[3])
            board.switch_turn()
            child = Node(board, node)
            node.add_child(child)


    #populate tree
    for d in range(depth):
        target_nodes = tree.get_nodes_of_depth(d)
        for node in target_nodes:
            create_children(node)

    
    #assign pointers
    def traverse(node):
        for child in node.get_children():
            traverse(child)

        if node.is_leaf():
            node.eval = node.get_data().piece_value_eval()
            return
        
        
        

    

    
    
    



if __name__ == '__main__':
    board = MinimaxBoard(50, ((0, 0, 0), (255, 255, 255)), ((255, 0, 0), (0, 0, 255)), ((50, 50, 50), (200, 200, 200)), (153, 122, 75))

    minimax(board, 5)
    

