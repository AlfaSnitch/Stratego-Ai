import pygame
import sys
import time

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

    def show_splash_screen(self):
        # Load the background image
        splash_bg = pygame.image.load('assests\\homepage_splash.jpg')
        
        splash_bg = pygame.transform.scale(splash_bg, (width, height))  # Scale to fit the screen

        splash_font = pygame.font.Font(None, 74)
        splash_text = splash_font.render(' ', True, (255, 255, 255))
        splash_rect = splash_text.get_rect(center=(width // 2, height // 2))

        self.screen.blit(splash_bg, (0, 0))  # Display the background image
        self.screen.blit(splash_text, splash_rect)  # Display text on top of the background
        pygame.display.update()

        time.sleep(1)  # Wait for 3 seconds
    
    def mainloop(self):
        
        message = ""
        game = self.game
        screen = self.screen
        dragger = self.game.dragger
        board = self.game.board
        sq = self.game.board.squares
        
        while True:
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            game.show_sidebar(screen,message)
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
                        
                        if motion_col<0 or motion_col >9:
                            continue
                        if motion_row<0 or motion_row>9:
                            continue
                        
                        
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
                        
                        if motion_col<0 or motion_col >9:
                            continue
                        if motion_row<0 or motion_row>9:
                            continue
                        
                        game.set_hover(motion_row,motion_col)
                        
                        if dragger.dragging:
                            dragger.update_mouse(event.pos)
                            #show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)
                            game.show_sidebar(screen, message)
                            if not (piece.color == 'blue' and piece.hidden):
                                game.show_hover(screen)
                                dragger.update_blit(screen)
                            
                    
                    #click release
                    elif event.type == pygame.MOUSEBUTTONUP:
                        
                        if dragger.dragging:
                            dragger.update_mouse(event.pos)
                            relaeased_row = dragger.mouseY // SQSIZE
                            relaeased_col = dragger.mouseX // SQSIZE
                            
                            if relaeased_col<0 or relaeased_col>9:
                                continue
                            if relaeased_row<0 or relaeased_row>9:
                                continue
                            
                            
                            # create possible move 
                            inital = Square(dragger.initial_row,dragger.initial_col,piece = sq[dragger.initial_row][dragger.initial_col].piece, value = sq[dragger.initial_row][dragger.initial_col].value)
                            final = Square(relaeased_row,relaeased_col)
                            move = Move(inital,final)
                            # print(inital.piece)
                            # check if valid move
                            if board.valid_move(dragger.piece,move):
                                m = self.game.evaluate_human_move(move)
                                
                                captured = board.squares[relaeased_row][relaeased_col].has_piece()
                                board.move(dragger.piece,move)
                            
                                game.show_sidebar(screen,m)
                                message = m
                                print(message)
                                #board.evaluate_board()
                                if board.gameover_by_win() or board.gameover_by_notmoving():
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
                    move = game.get_best_move(1)
                    initial_pos =move.initial 
                    final_pos = move.final
                    initial_square = board.squares[initial_pos.row][initial_pos.col]
                    final_square = board.squares[final_pos.row][final_pos.col]
           
                    piece = initial_square.piece
                    captured = final_square.has_piece()
                    board.ai_move(move)
                    #board.evaluate_board()
                    final = Square(final_pos.row,final_pos.col,piece=piece.name,value=piece.value)
                    if  board.gameover_by_win() or board.gameover_by_notmoving():
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
    
                
                    
            
            pygame.display.update()
main = Main()
main.show_splash_screen()
main.mainloop()
