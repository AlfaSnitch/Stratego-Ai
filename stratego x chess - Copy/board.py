from const import *
from square import Square
from piece import *

class Board:
    def __init__(self):
        self.squares = [ [0,0,0,0,0,0,0,0,0,0] for col in range(COLS) ]
        self._create()
        self._add_pieces('red')
        self._add_pieces('blue')
    
    def _create(self):
        
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row,col)
        
    def _add_pieces(self,color):
        row_pl = [0,1,2,3]
        row_ai = [9,8,7,6]
        
        grid = [ 
                 ['flag', 'bomb', 'miner', 'sergeant', 'miner', 'miner', 'miner', 'sergeant', 'miner', 'sergeant'],
                 ['bomb', 'scout', 'lieutenant', 'scout', 'lieutenant', 'captain', 'bomb', 'lieutenant', 'major', 'bomb'],
                 ['scout', 'major', 'scout', 'lieutenant', 'scout', 'captain', 'captain', 'spy', 'general', 'bomb'],
                 ['captain', 'scout', 'colonel', 'marshal', 'major', 'scout', 'colonel', 'bomb', 'sergeant', 'scout']
                ]

        # for organic player
        for r in row_pl:
            for c in range(COLS):
                s = grid[r][c]
                if(s == 'flag'):
                   self.squares[r][c] = Square(r,c,Flag(color))
                elif s=='bomb':
                    self.squares[r][c] = Square(r,c,Bomb(color)) 
                elif s=='miner':
                    self.squares[r][c] = Square(r,c,Miner(color)) 
                elif s=='sergeant':
                    self.squares[r][c] = Square(r,c,Sergeant(color)) 
                elif s=='scout':
                    self.squares[r][c] = Square(r,c,Scout(color)) 
                elif s=='major':
                    self.squares[r][c] = Square(r,c,Major(color)) 
                elif s=='colonel':
                    self.squares[r][c] = Square(r,c,Colonel(color)) 
                elif s=='captain':
                    self.squares[r][c] = Square(r,c,Captain(color)) 
                elif s=='spy':
                    self.squares[r][c] = Square(r,c,Spy(color)) 
                elif s=='marshal':
                    self.squares[r][c] = Square(r,c,Marshal(color)) 
                elif s=='lieutenant':
                    self.squares[r][c] = Square(r,c,Lieutenant(color)) 
                elif s=='general':
                    self.squares[r][c] = Square(r,c,General(color)) 
            
        # for ai 
        if(color == 'red'):
            for r in row_ai:
                r1 = abs(r-9)
                for c in range(COLS):
                    s = grid[r1][c]
                    if(s == 'flag'):
                        self.squares[r][c] = Square(r,c,Flag(color))
                    elif s=='bomb':
                        self.squares[r][c] = Square(r,c,Bomb(color)) 
                    elif s=='miner':
                        self.squares[r][c] = Square(r,c,Miner(color)) 
                    elif s=='sergeant':
                        self.squares[r][c] = Square(r,c,Sergeant(color)) 
                    elif s=='scout':
                        self.squares[r][c] = Square(r,c,Scout(color)) 
                    elif s=='major':
                        self.squares[r][c] = Square(r,c,Major(color)) 
                    elif s=='colonel':
                        self.squares[r][c] = Square(r,c,Colonel(color)) 
                    elif s=='captain':
                        self.squares[r][c] = Square(r,c,Captain(color)) 
                    elif s=='spy':
                        self.squares[r][c] = Square(r,c,Spy(color)) 
                    elif s=='marshal':
                        self.squares[r][c] = Square(r,c,Marshal(color)) 
                    elif s=='lieutenant':
                        self.squares[r][c] = Square(r,c,Lieutenant(color)) 
                    elif s=='general':
                        self.squares[r][c] = Square(r,c,General(color)) 


                
            