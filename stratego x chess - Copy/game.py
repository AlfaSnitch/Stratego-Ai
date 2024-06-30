import pygame
from const import *
from board import Board
from square import Square
from dragger import Dragger

# Constants

BACKGROUND_COLOR = (231, 212, 181)  # beige bg
GRID_COLOR = (0, 0, 0)  # Black grid lines

class Game:
    
    def __init__(self):
       self.board = Board()
       self.dragger = Dragger()
       self.next_player = 'red'
        
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
    
    def next_turn(self):
        if self.next_player == 'red':
            self.next_player = 'blue'
        else:
            self.next_player='red'