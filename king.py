from piece import Piece
import pygame

class King(Piece):
    def __init__(self, team, pos, game):
        super().__init__("king", team, pos, game)
        self.in_check = False

    def __repr__(self):
        return f"{self.team} king at ({self.pos})"
    
    def get_available_moves(self, piece_locations):
        self.available_moves_rect = []
        available_moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        for direction in directions:
            row = self.pos[0] + direction[0]
            col = self.pos[1] + direction[1]
            if 0 <= row < 8 and 0 <= col < 8:
                idx = row * 8 + col
                if piece_locations[idx] == 0:
                    available_moves.append([row, col])
                elif piece_locations[idx].team != self.team:
                    available_moves.append([row, col])

        return available_moves
    
    def draw_check(self):
        cell_width = self.settings.screen_width / 8
        cell_height = self.settings.screen_heigth / 8
        color = self.settings.checking_color
        thickness = self.settings.checking_thickness
        col = self.pos[1]
        row = self.pos[0]
        cell_rect = pygame.Rect(col * cell_width, row * cell_height, cell_width, cell_height)
        pygame.draw.rect(self.screen, color, cell_rect, thickness)