from piece import Piece
from rook import Rook
from bishop import Bishop
import pygame


class Queen(Piece):
    def __init__(self, team, pos, game):
        super().__init__("queen", team, pos, game)

    def __repr__(self):
        return f"{self.team} queen at ({self.pos})"
    
    def available_moves(self, piece_locations):
        rook_moves = Rook.available_moves(self, piece_locations)
        bishop_moves = Bishop.available_moves(self, piece_locations)

        available_moves = rook_moves + bishop_moves

        for move in available_moves:
            self.available_moves_rect.append(pygame.Rect(move[1] * 75, move[0] * 75, 75, 75))

        return available_moves