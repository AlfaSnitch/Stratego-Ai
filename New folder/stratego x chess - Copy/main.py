import pygame
import sys

from const import *
from game import Game
from square import Square
from move import Move


class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode( (width,height) )
        pygame.display.set_caption('Stratego')
        self.game = Game()

    def mainloop(self):
        
        game = self.game
        screen = self.screen
        dragger = self.game.dragger
        board = self.game.board
        
        while True:
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            
            game.show_hover(screen)
            
            if dragger.dragging:
                if not (piece.color == 'blue' and piece.hidden):              
                    dragger.update_blit(screen)
            
            for event in pygame.event.get():
                
                if event.type == pygame.KEYDOWN:
                    # restarting the game
                    if event.key == pygame.K_r:
                        game.reset()
                        game = self.game
                        dragger = self.game.dragger
                        board = self.game.board
                
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                elif game.next_player == 'red':
                     #click
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        dragger.update_mouse(event.pos)
                        
                        clicked_row = dragger.mouseY // SQSIZE
                        clicked_col = dragger.mouseX // SQSIZE
                        
                        if board.squares[clicked_row][clicked_col].has_piece():
                            piece = board.squares[clicked_row][clicked_col].piece
                            
                            #valid piece(color)?
                            if piece.color == game.next_player:
                                
                                board.cal_moves(piece, clicked_row, clicked_col)
                                dragger.save_initial(event.pos)
                                dragger.drag_piece(piece)
                                #show methods
                                game.show_bg(screen)
                                game.show_last_move(screen)
                                game.show_moves(screen)
                                game.show_pieces(screen)

                    
                    # motion 
                    elif event.type == pygame.MOUSEMOTION:
                        motion_row = event.pos[1]//SQSIZE
                        motion_col = event.pos[0]//SQSIZE
                        
                        game.set_hover(motion_row,motion_col)
                        
                        if dragger.dragging:
                            dragger.update_mouse(event.pos)
                            #show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)
                            if not (piece.color == 'blue' and piece.hidden):
                                game.show_hover(screen)
                                dragger.update_blit(screen)
                            
                    
                    #click release
                    elif event.type == pygame.MOUSEBUTTONUP:
                        
                        if dragger.dragging:
                            dragger.update_mouse(event.pos)
                            relaeased_row = dragger.mouseY // SQSIZE
                            relaeased_col = dragger.mouseX // SQSIZE
                            
                            # create possible move 
                            inital = Square(dragger.initial_row,dragger.initial_col)
                            final = Square(relaeased_row,relaeased_col)
                            move = Move(inital,final)
                            
                            # check if valid move
                            if board.valid_move(dragger.piece,move):
                                captured = board.squares[relaeased_row][relaeased_col].has_piece()
                                board.move(dragger.piece,move)
                                game.evaluate_human_move(move)
                                #board.evaluate_board()
                                if board.gameover_by_win(dragger.piece,move.final) or board.gameover_by_notmoving():
                                    game.reset()
                                    game = self.game
                                    dragger = self.game.dragger
                                    board = self.game.board
                                    
                                else:
                                    #draw                          
                                    game.play_sound(captured)
                                    game.show_bg(screen)
                                    game.show_last_move(screen)
                                    game.show_pieces(screen)
                                    #next turn
                                    game.next_turn()
                        
                        dragger.undrag_piece()
                
                elif game.next_player == 'blue':
                    move = game.get_best_move(4)
                    initial_pos =move.initial 
                    final_pos = move.final
                    initial_square = board.squares[initial_pos.row][initial_pos.col]
                    final_square = board.squares[final_pos.row][final_pos.col]
           
                    piece = initial_square.piece
                    captured = final_square.has_piece()
                    board.ai_move(move)
                    #board.evaluate_board()
                    final = Square(final_pos.row,final_pos.col)
                    if  board.gameover_by_win(piece,final) or board.gameover_by_notmoving():
                        game.reset()
                        game = self.game
                        board = self.game.board
                                    
                    else:
                         #draw                          
                        game.play_sound(captured)
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_pieces(screen)
                        #next turn
                        game.next_turn()
    
                
                    
            
            pygame.display.update()
main = Main()
main.mainloop()
