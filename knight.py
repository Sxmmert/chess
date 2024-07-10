from piece import Piece
import pygame

class Knight(Piece):
    def __init__(self, team, pos, game):
        super().__init__("knight", team, pos, game)

    def __repr__(self):
        return f"{self.team} knight at ({self.pos})"
    
    def get_available_moves(self):
        piece_locations = self.game.piece_locations
        self.available_moves_rect = []
        available_moves = []
        moves = [
            (-2, -1), (-2, 1), (2, -1), (2, 1),
            (-1, -2), (1, -2), (-1, 2), (1, 2)
        ]
        
        for move in moves:
            row, col = self.pos[0] + move[0], self.pos[1] + move[1]
            if 0 <= row < 8 and 0 <= col < 8:
                idx = row * 8 + col
                if piece_locations[idx] == 0 or piece_locations[idx].team != self.team:
                    available_moves.append([row, col])
        
        self.available_moves = available_moves
        self.make_rect()