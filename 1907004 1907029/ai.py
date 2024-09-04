# # import pygame
import copy

# # RED = (255,0,0)
# # BLUE = (0,0,255)

# def make_move(self, move):
#         new_board = copy.deepcopy(self)
#         initial_pos, final_pos = move
#         initial_square = new_board.squares[initial_pos[0]][initial_pos[1]]
#         final_square = new_board.squares[final_pos[0]][final_pos[1]]

#         if final_square.has_piece() and final_square.piece.color != initial_square.piece.color:
#             # Handle the attack logic
#             attacker = initial_square.piece
#             defender = final_square.piece
#             if attacker.value < defender.value:
#                 defender.reveal()
#                 # Attacker loses
#                 initial_square.piece = None
#             else:
#                 # Defender loses or tie
#                 final_square.piece = attacker
#                 initial_square.piece = None
#         else:
#             # Move to empty square
#             final_square.piece = initial_square.piece
#             initial_square.piece = None

#         return new_board


# def minimax(board, depth, alpha, beta, maximizing_player):
#     if depth == 0 or game_over(board):
#         return evaluate_board(board)

#     if maximizing_player:
#         max_eval = float('-inf')
#         for move in get_all_moves(board, 'red'):
#             new_board = make_move(board, move)
#             eval = minimax(new_board, depth - 1, alpha, beta, False)
#             max_eval = max(max_eval, eval)
#             alpha = max(alpha, eval)
#             if beta <= alpha:
#                 break
#         return max_eval
#     else:
#         min_eval = float('inf')
#         for move in get_all_moves(board, 'blue'):
#             new_board = make_move(board, move)
#             eval = minimax(new_board, depth - 1, alpha, beta, True)
#             min_eval = min(min_eval, eval)
#             beta = min(beta, eval)
#             if beta <= alpha:
#                 break
#         return min_eval

# # def get_all_moves(board, player):
# #     moves = []
# #     directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, down, left, right

# #     for row in range(len(board.squares)):
# #         for col in range(len(board.squares[row])):
# #             square = board.squares[row][col]
# #             if square.has_piece() and square.piece.color == player:
# #                 for d in directions:
# #                     new_row, new_col = row + d[0], col + d[1]
# #                     if 0 <= new_row < len(board.squares) and 0 <= new_col < len(board.squares[row]):
# #                         target_square = board.squares[new_row][new_col]
# #                         if not target_square.has_piece() or target_square.piece.color != player:
# #                             moves.append(((row, col), (new_row, new_col)))

# #     return moves


# # def evaluate_board(board):
# #     piece_values = {
# #         'marshal': 10,
# #         'general': 9,
# #         'colonel': 8,
# #         'major': 7,
# #         'captain': 6,
# #         'lieutenant': 5,
# #         'sergeant': 4,
# #         'miner': 3,
# #         'scout': 2,
# #         'spy': 1,
# #         'bomb': 11,
# #         'flag': 0
# #     }

# #     score = 0

# #     for row in board.squares:
# #         for square in row:
# #             if square.has_piece():
# #                 piece = square.piece
# #                 if piece.color == 'blue':
# #                     piece_value = piece_values[piece.type]

# #                     # Adjust the value based on specific strategic elements
# #                     if piece.type == 'spy':
# #                         piece_value += piece_values['marshal']  # Spy can take down Marshal
# #                     if piece.type == 'miner':
# #                         piece_value += piece_values['bomb']  # Miner can disarm bombs
# #                     if piece.type == 'scout':
# #                         piece_value += 1  # Scouts can detect higher-ranking pieces

# #                     score += piece_value

# #                 elif piece.color == 'red':
# #                     piece_value = piece_values[piece.type]

# #                     # Adjust the value based on specific strategic elements
# #                     if piece.type == 'spy':
# #                         piece_value -= piece_values['marshal']  # Spy can take down Marshal
# #                     if piece.type == 'miner':
# #                         piece_value -= piece_values['bomb']  # Miner can disarm bombs
# #                     if piece.type == 'scout':
# #                         piece_value -= 1  # Scouts can detect higher-ranking pieces

# #                     score -= piece_value

# #     return score
