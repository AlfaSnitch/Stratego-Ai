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
     
    
    def order_moves(self, moves):
    # Heuristic for move ordering: prioritize capturing important pieces, disarming bombs, and advancing pieces
        def move_value(move):
            initial_piece = move.initial.piece
            target_piece = move.final.piece

            value = 0

            # Capturing pieces
            if target_piece:
                value += target_piece.value * 10  # Prioritize capturing higher value pieces
                if target_piece.name == 'flag':
                    value += 1000  # Highest priority to capture the flag
                elif target_piece.name == 'marshal':
                    value += 500  # High priority to capture the marshal
                elif target_piece.name == 'bomb':
                    if initial_piece.name == 'miner':
                        value += 300  # Miners disarming bombs
                    else:
                        value += 200  # Capturing a bomb with other pieces


            # Advancing pieces
            if initial_piece.color == 'blue':
                value += move.final.row  # Prefer advancing towards the opponent's side for blue
            else:
                value += (len(self.board.squares) - move.final.row - 1)  # Prefer advancing towards the opponent's side for red

            # Scouting moves
            if initial_piece.name == 'scout' and target_piece:
                value += 1000 

            return value

        # Sort moves by the heuristic value in descending order
        return sorted(moves, key=move_value, reverse=True)
        
        
    def get_best_move(self, depth):
        best_move = None
        best_value = float('-inf') if self.next_player == 'blue' else float('inf')
        alpha = float('-inf')
        beta = float('inf')
        
        #get all possible moves 
        all_moves = self.board.get_all_moves(self.next_player)
        
        # order moves according to some heuristics
        ordered_moves = self.order_moves(all_moves)


        for move in ordered_moves:
            new_board = self.board.make_move(move)
            board_value = new_board.minimax(depth - 1, alpha, beta, self.next_player == 'red')
            if self.next_player == 'blue' and board_value > best_value:
                best_value = board_value
                best_move = move
            elif self.next_player == 'red' and board_value < best_value:
                best_value = board_value
                best_move = move
            if self.next_player == 'blue':
                alpha = max(alpha, board_value)
            else:
                beta = min(beta, board_value)
            if beta <= alpha:
                break

        return best_move

    
        