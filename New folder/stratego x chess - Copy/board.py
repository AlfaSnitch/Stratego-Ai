import copy
from const import *
from square import Square
from piece import *
import math
from move import Move

class Board:
    def __init__(self):
        self.squares = [ [0,0,0,0,0,0,0,0,0,0] for col in range(COLS) ]
        self.last_move = None
        self._create()
        self._add_pieces('red')
        self._add_pieces('blue')
    

        
    def evaluate_board(board):
        piece_values = {
            'marshal': 10,
            'general': 9,
            'colonel': 8,
            'major': 7,
            'captain': 6,
            'lieutenant': 5,
            'sergeant': 4,
            'miner': 3,
            'scout': 2,
            'spy': 1,
            'bomb': 5,
            'flag': 1000
        }

        score = 0

        for row in board.squares:
            for square in row:
                if square.has_piece():
                    piece = square.piece
                    if piece.color == 'not':
                        score += piece_values[piece.name]
                        if not piece.revealed:
                            if piece.name == 'scout':
                                score += 2  # Scouts revealing pieces
                            elif piece.name == 'miner':
                                score += 3  # Miners disarming bombs
                            elif piece.name == 'spy' and piece.value == 1:  # Spy has unique capture ability
                                score += 5
                    elif piece.color == 'red':
                        score -= piece_values[piece.name]
                        if piece.revealed:
                            if piece.name == 'scout':
                                score -= 2  # Scouts revealing pieces
                            elif piece.name == 'miner':
                                score -= 3  # Miners disarming bombs
                            elif piece.name == 'spy' and piece.value == 1:  # Spy has unique capture ability
                                score -= 5

        return score


    
    def minimax(board, depth, alpha, beta, maximizing_player):
        if depth == 0 or board.gameover_by_notmoving():
            return board.evaluate_board()

        if maximizing_player:
            max_eval = -math.inf
            for move in board.get_all_moves('blue'):
                new_board = board.make_move(move)
                eval = new_board.minimax(depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = math.inf
            for move in board.get_all_moves('red'):
                new_board = board.make_move(move)
                eval = new_board.minimax(depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

        
    
    def get_all_moves(board, player):
        moves = []

        for row in range(len(board.squares)):
            for col in range(len(board.squares[row])):
                square = board.squares[row][col]
                if square.has_piece() and square.piece.color == player:
                    piece = square.piece

                    # Skip bombs and flags
                    if piece.name in ['bomb', 'flag']:
                        continue

                    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

                    for dr, dc in directions:
                        if piece.name == 'scout':
                            for step in range(1, len(board.squares)):
                                new_row, new_col = row + step * dr, col + step * dc
                                if 0 <= new_row < len(board.squares) and 0 <= new_col < len(board.squares[row]):
                                    target_square = board.squares[new_row][new_col]
                                    if target_square.has_piece():
                                        if target_square.piece.color != player:
                                            moves.append(Move(square, target_square))
                                        break
                                    else:
                                        moves.append(Move(square, target_square))
                        else:
                            new_row, new_col = row + dr, col + dc
                            if 0 <= new_row < len(board.squares) and 0 <= new_col < len(board.squares[row]):
                                target_square = board.squares[new_row][new_col]
                                if not target_square.has_piece() or target_square.piece.color != player:
                                    moves.append(Move(square, target_square))

        return moves
    
    

    def make_move(self, move):
        new_board = copy.deepcopy(self)
        initial = move.initial
        final = move.final
        i = new_board.squares[initial.row][initial.col]
        j = new_board.squares[final.row][final.col]


        # Check for piece interaction
        if j.piece is not None:
            if j.piece.color == 'red' and i.piece.color == 'blue':
                if i.piece.name == 'spy' and j.piece.name == 'marshal':
                    j.piece = i.piece
                    j.value = i.value
                    i.piece = None 
                    i.value = 0  
                elif j.piece.name == 'bomb' and i.piece.name == 'miner':
                    j.piece = i.piece
                    j.value = i.value
                    i.piece = None # Bomb captures everything except Miner
                    i.value = 0
                elif j.value > i.piece.value:
                    i.piece = None  
                    i.value = 0
                    j.piece.revealed()
                elif i.value > j.value:
                    j.piece = i.piece
                    j.value = i.value
                    i.piece = None
                    i.value = 0
                elif i.value == j.value:
                    j.value = i.value = 0
                    j.piece = i.piece = None
            elif j.piece.color == 'blue' and i.piece.color == 'red':
            
                if i.piece.name == 'spy' and j.piece.name == 'marshal':
                    j.piece = i.piece
                    j.value = i.value
                    i.piece = None 
                    i.value = 0  
                elif j.piece.name == 'bomb' and i.piece.name == 'miner':
                    j.piece = i.piece
                    j.value = i.value
                    i.piece = None # Bomb captures everything except Miner
                    i.value = 0
                elif j.value > i.piece.value:
                    i.piece = None  
                    i.value = 0
                    j.piece.revealed()
                elif i.value > j.value:
                    j.piece = i.piece
                    j.value = i.value
                    i.piece = None
                    i.value = 0
                elif i.value == j.value:
                    j.value = i.value = 0
                    j.piece = i.piece = None
            
        else:
            j.piece = i.piece
            j.value = i.value
            i.value = 0
            i.piece = None
            
        return new_board
 
 
    def ai_move(self, move):

        initial_pos=move.initial
        final_pos = move.final
        i = self.squares[initial_pos.row][initial_pos.col]
        j = self.squares[final_pos.row][final_pos.col]

        i.piece.moved = True 
        
        flag = False

        if isinstance(i.piece,Miner) and isinstance(j.piece,Bomb):
            j.piece = i.piece 
            j.value = i.value
            i.value = 0
            i.piece = None
        elif isinstance(i.piece, Spy) and isinstance(j.piece, Marshal):
            j.piece = i.piece 
            j.value = i.value
            i.value = 0
            i.piece = None
        elif i.value >= j.value:
            flag = True
        
        if flag:
            x = i.value
            y = j.value
            if j.has_piece() and x > y:
                j.piece = i.piece 
                j.value = x
                i.value = 0
                i.piece = None
            
            elif j.has_piece() and x == y:
                j.piece = None
                j.value = 0
                i.value = 0   
                i.piece = None
            else:
                j.piece = i.piece 
                x = i.value
                j.value = x
                i.value = 0
                i.piece = None
        elif j.value > i.value:
            i.piece = None
            i.value = 0
            piece = j.piece
            piece.revealed()
            # move
   
        #set last move
        self.last_move = move
        
        # if final_square.has_piece() and final_square.piece.color != initial_square.piece.color:
        #     # Handle the attack logic
        #     attacker = initial_square.piece
        #     defender = final_square.piece
        #     if attacker.value < defender.value:
        #         defender.revealed()
        #         # Attacker loses
        #         initial_square.piece = None
        #     else:
        #         # Defender loses or tie
        #         final_square.piece = attacker
        #         initial_square.piece = None
        # else:
        #     # Move to empty square
        #     final_square.piece = initial_square.piece
        #     initial_square.piece = None

    

    '''
    def make_move(self, move):
        new_board = copy.deepcopy(self)
        
        initial, final = move
        i = new_board.squares[initial.row][initial.col]
        j = new_board.squares[final.row][final.col]
        var = j.piece

        flag = False

        if isinstance(i.piece,Miner) and isinstance(j.piece,Bomb):
            j.piece = i.piece 
            j.value = i.value
            i.value = 0
            i.piece = None
        elif isinstance(i.piece, Spy) and isinstance(j.piece, Marshal):
            j.piece = i.piece 
            j.value = i.value
            i.value = 0
            i.piece = None
        elif i.value >= j.value:
            flag = True
        
        if flag:
            x = i.value
            y = j.value
            if j.has_piece() and x > y:
                j.piece = i.piece 
                j.value = x
                i.value = 0
                i.piece = None
            
            elif j.has_piece() and x == y:
                j.piece = None
                j.value = 0
                i.value = 0   
                i.piece = None
            else:
                j.piece = i.piece 
                x = i.value
                j.value = x
                i.value = 0
                i.piece = None
        elif j.value > i.value:
            i.piece = None
            i.value = 0
            var.revealed()
            
        i.piece.moved = True    
            # clear valid move
        i.piece.clear_moves()
            #set last move
        self.last_move = move
        

        return new_board
'''
    
    # def evaluate_board(self):
    #     score = 0
    #     for row in self.squares:
    #         for square in row:
    #             if square.has_piece():
    #                 piece = square.piece
    #                 if not piece == None:
    #                     if piece.color == 'blue':
    #                         score += piece.value
    #                     elif piece.color == 'red':
    #                         score -= piece.value
    #     return score

    def gameover_by_notmoving(self):
        red_move = False
        blue_move = False
        for i in range(ROWS):
            for j in range(COLS):
                piece = self.squares[i][j].piece
                if not piece == None:
                    if piece.color == 'red' and self.squares[i][j].value>0:
                        red_move = True
                    elif piece.color == 'blue' and self.squares[i][j].value>0:
                        blue_move = True
        
        return not red_move or not blue_move
                
    
    def gameover_by_win(self,piece,final):
        red_flag = blue_flag = False
        red_has_moves = blue_has_moves = False
        
        j = self.squares[final.row][final.col]
        
        if isinstance(j.piece,Flag):
            if piece.color == 'red':
                print('red wins')
                return True
            else: 
                print('blue wins')
                return True
        return False
                
        
            
    
    def move(self, piece, move):
        initial = move.initial
        final = move.final
        
        # console board move update
        i = self.squares[initial.row][initial.col]
        j = self.squares[final.row][final.col]
        var = j.piece
        
        flag = False

        if isinstance(i.piece,Miner) and isinstance(j.piece,Bomb):
            j.piece = piece 
            j.value = i.value
            i.value = 0
            i.piece = None
        elif isinstance(i.piece, Spy) and isinstance(j.piece, Marshal):
            j.piece = piece 
            j.value = i.value
            i.value = 0
            i.piece = None
        elif i.value >= j.value:
            flag = True
        
        if flag:
            x = i.value
            y = j.value
            if j.has_piece() and x > y:
                j.piece = piece 
                j.value = x
                i.value = 0
                i.piece = None
            
            elif j.has_piece() and x == y:
                j.piece = None
                j.value = 0
                i.value = 0   
                i.piece = None
            else:
                j.piece = piece 
                x = i.value
                j.value = x
                i.value = 0
                i.piece = None
        elif j.value > i.value:
            i.piece = None
            i.value = 0
            var.revealed()
            # move
        piece.moved = True    
            # clear valid move
        piece.clear_moves()
            #set last move
        self.last_move = move
    
        
 
    def valid_move(self,piece,move):
        return move in piece.moves
    
    
    def cal_moves(self,piece,row,col):
        
        def stright_line_moves(incrs):
            for incr in incrs:
                row_incr,col_incr = incr
                possible_move_row = row+row_incr
                possible_move_col = col+col_incr
                
                while True:
                    
                    if Square.in_range(possible_move_row, possible_move_col):
                        # create squares of the possible new move
                        initial = Square(row,col)
                        final = Square(possible_move_row,possible_move_col)
                        # create a possible new move
                        move = Move(initial,final)
                        
                        #empty
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            # append moves
                            piece.add_move(move)
                        
                        #has enemy piece, add moves and break
                        if self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color):
                            piece.add_move(move)
                            break 
                        # has team piece == breaks
                        if self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break 
                    # not in range
                    else:
                        break
                        
                    #incrementing incurs
                    possible_move_row = possible_move_row +row_incr
                    possible_move_col = possible_move_col+col_incr

        def piece_move():
            adjs = [
                (row+1,col),(row-1,col),(row,col+1),(row,col-1)
            ]
            
            for possible_move in adjs:
                possible_move_row, possible_move_col = possible_move
                if Square.in_range(possible_move_row,possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.color):
                        initial = Square(row,col)
                        final = Square(possible_move_row,possible_move_col)
                        
                        move = Move(initial,final)
                        
                        piece.add_move(move)
            

        
        if isinstance(piece,Scout):
            stright_line_moves([
                (-1,0), # up 
                (0,1), # left
                (1,0), # down
                (0,-1) # right
            ])
        
        elif isinstance(piece,Bomb):
            pass
        elif isinstance(piece,Flag):
            pass
        else:
            piece_move()
    
    
    def _create(self):
        
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row,col)
        
        
    def _add_pieces(self,color):
        row_pl = [0,1,2,3]
        row_ai = [9,8,7,6]
        '''
        grid = [ 
                 ['flag', 'bomb', 'miner', 'sergeant', 'miner', 'miner', 'miner', 'sergeant', 'miner', 'sergeant'],
                 ['bomb', 'scout', 'lieutenant', 'scout', 'lieutenant', 'captain', 'bomb', 'lieutenant', 'major', 'bomb'],
                 ['scout', 'major', 'scout', 'lieutenant', 'scout', 'captain', 'captain', 'spy', 'general', 'bomb'],
                 ['bomb', 'bomb', 'bomb', 'bomb', 'bomb','bomb', 'bomb', 'bomb', 'bomb', 'bomb']
        ]
        '''
        grid = [ 
                 ['flag', 'bomb', 'miner', 'sergeant', 'miner', 'miner', 'miner', 'sergeant', 'miner', 'sergeant'],
                 ['bomb', 'scout', 'lieutenant', 'scout', 'lieutenant', 'captain', 'bomb', 'lieutenant', 'major', 'bomb'],
                 ['scout', 'major', 'scout', 'lieutenant', 'scout', 'captain', 'captain', 'spy', 'general', 'bomb'],
                 ['captain', 'scout', 'colonel', 'marshal', 'major', 'scout', 'colonel', 'bomb', 'sergeant', 'spy']
                ]
       
        # for organic player
        for r in row_pl:
            for c in range(COLS):
                s = grid[r][c]
                if(s == 'flag'):
                   self.squares[r][c] = Square(r,c,0,Flag(color))
                elif s=='bomb':
                    self.squares[r][c] = Square(r,c,11,Bomb(color)) 
                elif s=='miner':
                    self.squares[r][c] = Square(r,c,3,Miner(color)) 
                elif s=='sergeant':
                    self.squares[r][c] = Square(r,c,4,Sergeant(color)) 
                elif s=='scout':
                    self.squares[r][c] = Square(r,c,2,Scout(color)) 
                elif s=='major':
                    self.squares[r][c] = Square(r,c,7,Major(color)) 
                elif s=='colonel':
                    self.squares[r][c] = Square(r,c,8,Colonel(color)) 
                elif s=='captain':
                    self.squares[r][c] = Square(r,c,6,Captain(color)) 
                elif s=='spy':
                    self.squares[r][c] = Square(r,c,1,Spy(color)) 
                elif s=='marshal':
                    self.squares[r][c] = Square(r,c,10,Marshal(color)) 
                elif s=='lieutenant':
                    self.squares[r][c] = Square(r,c,5,Lieutenant(color)) 
                elif s=='general':
                    self.squares[r][c] = Square(r,c,9,General(color)) 
            
        # for ai 
        if(color == 'red'):

            for r in row_ai:
                r1 = abs(r-9)
                for c in range(COLS):
                    s = grid[r1][c]
                    if(s == 'flag'):
                        self.squares[r][c] = Square(r,c,0,Flag(color))
                    elif s=='bomb':
                        self.squares[r][c] = Square(r,c,11,Bomb(color)) 
                    elif s=='miner':
                        self.squares[r][c] = Square(r,c,3,Miner(color)) 
                    elif s=='sergeant':
                        self.squares[r][c] = Square(r,c,4,Sergeant(color)) 
                    elif s=='scout':
                        self.squares[r][c] = Square(r,c,2,Scout(color)) 
                    elif s=='major':
                        self.squares[r][c] = Square(r,c,7,Major(color)) 
                    elif s=='colonel':
                        self.squares[r][c] = Square(r,c,8,Colonel(color)) 
                    elif s=='captain':
                        self.squares[r][c] = Square(r,c,6,Captain(color)) 
                    elif s=='spy':
                        self.squares[r][c] = Square(r,c,1,Spy(color)) 
                    elif s=='marshal':
                        self.squares[r][c] = Square(r,c,10,Marshal(color)) 
                    elif s=='lieutenant':
                        self.squares[r][c] = Square(r,c,5,Lieutenant(color)) 
                    elif s=='general':
                        self.squares[r][c] = Square(r,c,9,General(color)) 


