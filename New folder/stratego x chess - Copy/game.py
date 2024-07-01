import pygame
from const import *
from board import Board
from square import Square
from dragger import Dragger

from config import Config
# Constants

BACKGROUND_COLOR = (231, 212, 181)  # beige bg
GRID_COLOR = (0, 0, 0)  # Black grid lines

class Game:
    
    def __init__(self):
       self.board = Board()
       self.dragger = Dragger()
       self.next_player = 'red'
       self.hovered_sqr = None
       self.config = Config()
        
    # Show methods
    
    def show_bg(self,surface):
        # Fill the background with a single color
        surface.fill(BACKGROUND_COLOR)
        # Draw the grid lines
        for row in range(ROWS):
            for col in range(COLS):
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, GRID_COLOR, rect, 1)  # '1' makes it an outlined rectangle
                
    def show_pieces(self,surface):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    
                    # all piece except dragger piece
                    if piece is not self.dragger.piece:
                        if 'blue' == piece.color and piece.hidden:
                            color = (150, 201, 244) if (row +col)%2 ==0 else (63, 162, 246)
                            pygame.draw.rect(surface, color, pygame.Rect(col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE),width=5)
                        else:
                            img = pygame.image.load(piece.texture)
                            img_center = col*SQSIZE + SQSIZE//2 , row*SQSIZE+SQSIZE//2
                            
                            piece.texture_rect = img.get_rect(center= img_center)
                            surface.blit(img,piece.texture_rect)

    
    def show_moves(self,surface):
        if self.dragger.dragging:
            piece = self.dragger.piece
            
            #loop through all possible moves
            for move in piece.moves:
                #color
                color = '#ECB176' if (move.final.row + move.final.col)%2 ==0 else '#A67B5B'
                # rect 
                rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
                #blit
                pygame.draw.rect(surface, color, rect)
                
    def show_last_move(self,surface):
        
        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final
            
            for pos in [initial,final]:
                #color
                color = (175, 143, 111) 
                # rect 
                rect = (pos.col*SQSIZE,pos.row*SQSIZE,SQSIZE,SQSIZE)
                #blit
                pygame.draw.rect(surface, color, rect)
    
    def show_hover(self,surface):
        if self.hovered_sqr:
            #color
                color = (180,180,180)
                # rect 
                rect = (self.hovered_sqr.col*SQSIZE,self.hovered_sqr.row*SQSIZE,SQSIZE,SQSIZE)
                #blit
                pygame.draw.rect(surface, color, rect,width=3)
            
    
    def next_turn(self):
        if self.next_player == 'red':
            self.next_player = 'blue'
        else:
            self.next_player='red'
    
    def set_hover(self,row,col):
        self.hovered_sqr = self.board.squares[row][col]
        
    def play_sound(self,captured=False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()
            
    def reset(self):
        self.__init__()
    
        