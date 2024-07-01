import pygame

RED = (255,0,0)
BLUE = (0,0,255)

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
        'bomb': -1,
        'flag': 0
    }

    score = 0

    for row in board.squares:
        for square in row:
            if square.has_piece():
                piece = square.piece
                if piece.color == 'blue':
                    piece_value = piece_values[piece.type]

                    # Adjust the value based on specific strategic elements
                    if piece.type == 'spy':
                        piece_value += piece_values['marshal']  # Spy can take down Marshal
                    if piece.type == 'miner':
                        piece_value += piece_values['bomb']  # Miner can disarm bombs
                    if piece.type == 'scout':
                        piece_value += 1  # Scouts can detect higher-ranking pieces

                    score += piece_value

                elif piece.color == 'red':
                    piece_value = piece_values[piece.type]

                    # Adjust the value based on specific strategic elements
                    if piece.type == 'spy':
                        piece_value -= piece_values['marshal']  # Spy can take down Marshal
                    if piece.type == 'miner':
                        piece_value -= piece_values['bomb']  # Miner can disarm bombs
                    if piece.type == 'scout':
                        piece_value -= 1  # Scouts can detect higher-ranking pieces

                    score -= piece_value

    return score
