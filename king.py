from piece import Piece
from rook import Rook
import pygame

class King(Piece):
    def __init__(self, team, pos, game):
        super().__init__("king", team, pos, game)
        self.in_check = False
        self.first_move = True
        self.castle_kingside_pos = None
        self.castle_queenside_pos = None

    def __repr__(self):
        return f"{self.team} king at ({self.pos})"
    
    def get_available_moves(self, piece_locations):
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

        if not self.first_move or self.in_check: return available_moves

        row = 7 if self.team == "white" else 0

        if self.can_castle_kingside(piece_locations):
            self.castle_kingside_pos = [row, 6]
            available_moves.append([row, 6])

        if self.can_castle_queenside(piece_locations):
            self.castle_queenside_pos = [row, 2]
            available_moves.append(self.castle_queenside_pos)

        return available_moves
    
    def is_rook_ready_for_castling(self, rook_position, piece_locations):
        piece = piece_locations[rook_position]
        return isinstance(piece, Rook) and piece.first_move

    def are_castling_squares_empty(self, squares, piece_locations):
        return all(piece_locations[pos] == 0 for pos in squares)
    
    def is_square_under_attack(self, pos, team):
        available_moves = self.game.black_moves if team == "white" else self.game.white_moves
        if available_moves == None: return
        return pos in available_moves

    def can_castle_kingside(self, piece_locations):
        rook_pos, empty_squares = (63, [61, 62]) if self.team == "white" else (7, [5, 6])
        for empty_square in empty_squares:
            pos = [empty_square // 8, empty_square % 8]
            if self.is_square_under_attack(pos, self.team):
                return False
        return self.is_rook_ready_for_castling(rook_pos, piece_locations) and self.are_castling_squares_empty(empty_squares, piece_locations)

    def can_castle_queenside(self, piece_locations):
        rook_pos, empty_squares = (56, [57, 58, 59]) if self.team == "white" else (0, [1, 2, 3])
        for empty_square in empty_squares:
            idx = Piece.index_to_pos(self, empty_square)
            if self.is_square_under_attack(idx, self.team):
                return False
        return self.is_rook_ready_for_castling(rook_pos, piece_locations) and self.are_castling_squares_empty(empty_squares, piece_locations)

    def draw_check(self):
        cell_width = self.settings.screen_width / 8
        cell_height = self.settings.screen_heigth / 8
        color = self.settings.checking_color
        thickness = self.settings.checking_thickness
        col = self.pos[1]
        row = self.pos[0]
        cell_rect = pygame.Rect(col * cell_width, row * cell_height, cell_width, cell_height)
        pygame.draw.rect(self.screen, color, cell_rect, thickness)

    def move(self, clicked_idx):
        super().move(clicked_idx)

        if self.castle_kingside_pos != None:
            castle_kingside_idx = Piece.pos_to_idx(self, self.castle_kingside_pos)
            if clicked_idx == castle_kingside_idx:
                if self.team == "white":
                    self.update_rook_position(63, 61, [7, 5])
                else:
                    self.update_rook_position(7, 5, [0, 5])

                self.settings.castle_sound.play()

        if self.castle_queenside_pos != None:
            castle_queenside_idx = Piece.pos_to_idx(self, self.castle_queenside_pos)
            if clicked_idx == castle_queenside_idx:
                if self.team == "white":
                    self.update_rook_position(56, 59, [7, 3])
                else:
                    self.update_rook_position(0, 3, [0, 3])

                self.settings.castle_sound.play()

        self.first_move = False
        self.castle_queenside_pos = None
        self.castle_kingside_pos = None

        self.game.white_moves = self.game.get_all_moves("white", self.game.piece_locations)
        self.game.black_moves = self.game.get_all_moves("black", self.game.piece_locations)
        if self.game.is_king_in_check("white") or self.game.is_king_in_check("black"):
            self.settings.check_sound.play()

    def update_rook_position(self, rook_start_idx, rook_end_idx, rook_end_pos):
        self.game.piece_locations[rook_end_idx] = self.game.piece_locations[rook_start_idx]
        self.game.piece_locations[rook_end_idx].idx = rook_end_idx
        self.game.piece_locations[rook_end_idx].pos = rook_end_pos
        self.game.piece_locations[rook_start_idx] = 0