from const import *
from square import Square
from piece import *

from move import Move

class Board:
    def __init__(self):
        self.squares = [ [0,0,0,0,0,0,0,0,0,0] for col in range(COLS) ]
        self.last_move = None
        self._create()
        self._add_pieces('red')
        self._add_pieces('blue')
    
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
                self.squares[row][col] = Square(row,col,-1)
        
    def _add_pieces(self,color):
        row_pl = [0,1,2,3]
        row_ai = [9,8,7,6]
        
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


                
            