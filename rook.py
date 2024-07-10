from piece import Piece
import pygame

class Rook(Piece):
    def __init__(self, team, pos, game):
        super().__init__("rook", team, pos, game)
        

    def __repr__(self):
        return f"{self.team} rook at ({self.pos})"
    
    def get_available_moves(self):
        piece_locations = self.game.piece_locations
        self.available_moves_rect = []
        available_moves = []

        # Define direction vectors for rook movements
        directions = [
            (1, 0), (-1, 0), (0, 1), (0, -1)  # Rook directions
        ]

        for direction in directions:
            for distance in range(1, 8):
                row = self.pos[0] + direction[0] * distance
                col = self.pos[1] + direction[1] * distance
                if 0 <= row < 8 and 0 <= col < 8:
                    idx = row * 8 + col
                    if piece_locations[idx] == 0:
                        available_moves.append([row, col])
                    elif piece_locations[idx].team != self.team:
                        available_moves.append([row, col])
                        break
                    else:
                        break
                else:
                    break

        self.available_moves = available_moves
        self.make_rect()