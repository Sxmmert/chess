from piece import Piece
import pygame

class Bishop(Piece):
    def __init__(self, team, pos, game):
        super().__init__("bishop", team, pos, game)

    def __repr__(self):
        return f"{self.team} bishop at ({self.pos})"
    
    def available_moves(self, piece_locations):
        self.available_moves_rect = []
        available_moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for direction in directions:
            row, col = self.pos
            while 1:
                row += direction[0]
                col += direction[1]
                if 0 <= row < 8 and 0 <= col < 8:
                    idx = row * 8 + col
                    if piece_locations[idx] == 0:
                        available_moves.append([row, col])
                    else:
                        if piece_locations[idx].team != self.team:
                            available_moves.append([row, col])
                        break
                else:
                    break

        for move in available_moves:
            self.available_moves_rect.append(pygame.Rect(move[1] * 75, move[0] * 75, 75, 75))
        
        return available_moves