from piece import Piece
from queen import Queen
from bishop import Bishop
from rook import Rook
from knight import Knight
import pygame

class Pawn(Piece):
    def __init__(self, team, pos, game):
        super().__init__("pawn", team, pos, game)
        self.first_move = True
        self.en_passant_move = None
        self.pawn_promotion = False

    def __repr__(self):
        return f"{self.team} pawn at ({self.pos})"
    
    def __eq__(self, other):
        if isinstance(other, Pawn):
            return self.team == other.team and self.name == other.name and self.pos == other.pos
        return False
      
    def move(self, clicked_idx):
        super().move(clicked_idx)
        self.first_move = False
        if self.en_passant_move is not None:
            if self.pos == self.en_passant_move:
                if self.team == "white":
                    taken_piece = self.game.piece_locations[self.idx + 8] 
                    self.game.piece_locations[self.idx + 8] = 0
                else:
                    taken_piece = self.game.piece_locations[self.idx - 8]
                    self.game.piece_locations[self.idx - 8] = 0

                self.game.en_passant_move = None
                self.game.taken_pieces.append(taken_piece)
                self.settings.capture_sound.play()

        if self.pos[0] == 0 or self.pos[0] == 7:
            self.pawn_promotion = True
            self.game.turn *= -1

        self.game.white_moves = self.game.get_all_moves("white", self.game.piece_locations)
        self.game.black_moves = self.game.get_all_moves("black", self.game.piece_locations)
        if self.game.is_king_in_check("white") or self.game.is_king_in_check("black"):
            self.settings.check_sound.play()

    def get_available_moves(self, piece_locations, en_passant_enabled = True):
        piece_location = int(self.pos[0] * 8 + self.pos[1])
        piece_step = -8 if self.team == "white" else 8
        en_passant_move = []
        available_moves = []
        en_passant = False

        if 0 <= piece_location + piece_step < 64 and piece_locations[int(piece_location + piece_step)] == 0:
            available_moves.append([(piece_location + piece_step) // 8, (piece_location + piece_step) % 8])
            if self.first_move and piece_locations[piece_location + (piece_step * 2)] == 0:
                available_moves.append([(piece_location + (piece_step * 2)) // 8, (piece_location + (piece_step * 2)) % 8])

        diagonal_offsets = [-9, -7] if self.team == "white" else [7, 9]
        for offset in diagonal_offsets:
            diag_pos = piece_location + offset
            if 0 <= diag_pos < 64 and piece_locations[diag_pos] != 0:
                rank_dif = piece_locations[diag_pos].pos[0] - self.pos[0]
                if abs(rank_dif) != 1: continue
                target_piece = piece_locations[diag_pos]
                if target_piece.team != self.team:
                    available_moves.append([diag_pos // 8, diag_pos % 8])

        if isinstance(self.game.last_moved, Pawn) and en_passant_enabled:
            double_jump = self.game.last_move_from[0] + self.game.last_move_to[0]
            if (double_jump == 4 or double_jump == 10) and self.pos[0] == self.game.last_move_to[0]:
                if(self.pos[1] - 1 == self.game.last_move_to[1]):
                    if(self.team == "white"):
                        en_passant_move = [self.pos[0] - 1, self.pos[1] - 1]
                        available_moves.append(en_passant_move)
                    else:
                        en_passant_move = [self.pos[0] + 1, self.pos[1] - 1]
                        available_moves.append(en_passant_move)
                    en_passant = True
                    
                if(self.pos[1] + 1 == self.game.last_move_to[1]):
                    if(self.team == "white"):
                        en_passant_move = [self.pos[0] - 1, self.pos[1] + 1]
                        available_moves.append(en_passant_move)
                    else:
                        en_passant_move = [self.pos[0] + 1, self.pos[1] + 1]
                        available_moves.append(en_passant_move)
                    en_passant = True

            self.en_passant_move = en_passant_move if en_passant else None

        return available_moves

    def draw_promotion(self):
        grid_width = self.settings.screen_width // 8
        grid_height = self.settings.screen_heigth // 8
        
        rect_width = grid_width
        rect_height = grid_height * 4 + grid_height // 2

        rect_x = self.pos[1] * rect_width
        rect_y = 0 if self.team == "white" else self.settings.screen_heigth - rect_height
        
        promotion_rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
        pygame.draw.rect(self.game.screen, self.settings.promotion_bg_color, promotion_rect)

        img_queen = pygame.image.load(f"img/queen_{'w' if self.team == "white" else "b"}.svg")
        img_queen = pygame.transform.scale(img_queen, (self.grid_width / 1.5, self.grid_height / 1.5))
        img_knight = pygame.image.load(f"img/knight_{'w' if self.team == "white" else "b"}.svg")
        img_knight = pygame.transform.scale(img_knight, (self.grid_width / 1.5, self.grid_height / 1.5))
        img_rook = pygame.image.load(f"img/rook_{'w' if self.team == "white" else "b"}.svg")
        img_rook = pygame.transform.scale(img_rook, (self.grid_width / 1.5, self.grid_height / 1.5))
        img_bishop = pygame.image.load(f"img/bishop_{'w' if self.team == "white" else "b"}.svg")
        img_bishop = pygame.transform.scale(img_bishop, (self.grid_width / 1.5, self.grid_height / 1.5))

        imgs = [img_queen, img_knight, img_rook, img_bishop] if self.team == "white" else [img_bishop, img_rook, img_knight, img_queen]

        x, y = 0, 0
        if self.team == "white":
            for i in range(4):
                x = rect_x + (grid_height - imgs[i].get_height()) // 2
                y = (grid_width - self.img.get_width()) // 2 + grid_height * i
                self.screen.blit(imgs[i], (x, y))

            marge = grid_width // 7.5
            start_y = (self.pos[0] + 4) * grid_height + marge
            start_x = self.pos[1] * grid_width + marge
            end_y = ((self.pos[0] + 4) * grid_height) + grid_height // 2 - marge
            end_x = (self.pos[1] + 1) * grid_width - marge

            pygame.draw.line(self.screen, self.settings.promotion_cross_color, 
                             (start_x, start_y), (end_x, end_y), self.settings.promotion_cross_thickness)
        
            start_x, end_x = end_x, start_x

            pygame.draw.line(self.screen, self.settings.promotion_cross_color, 
                             (start_x, start_y), (end_x, end_y), self.settings.promotion_cross_thickness)
        else:
            for i in range(4):
                x = rect_x + (grid_height - imgs[i].get_height()) // 2
                y = (grid_width - self.img.get_width()) // 2 + grid_height * (i + 4)
                self.screen.blit(imgs[i], (x, y))

            start_y = (self.pos[0] - 4) * grid_height + (grid_height // 2)
            start_x = (self.pos[1] + 1) * grid_width
            end_y = ((self.pos[0] - 4) * grid_height) + grid_height
            end_x = self.pos[1] * grid_width

            pygame.draw.line(self.screen, self.settings.promotion_cross_color, 
                             (start_x, start_y), (end_x, end_y), self.settings.promotion_cross_thickness)
        
            start_x, end_x = end_x, start_x

            pygame.draw.line(self.screen, self.settings.promotion_cross_color, 
                             (start_x, start_y), (end_x, end_y), self.settings.promotion_cross_thickness)   

    def get_promotion_rect(self):
        rects = {}
        height = self.game.settings.screen_heigth // 8
        width = self.game.settings.screen_width // 8

        if self.team == "white":
            rects[Queen(self.team, self.pos, self.game)] = self.pos_to_rect(self.pos)
            rects[Knight(self.team, self.pos, self.game)] = self.pos_to_rect([self.pos[0] + 1, self.pos[1]])
            rects[Rook(self.team, self.pos, self.game)] = self.pos_to_rect([self.pos[0] + 2, self.pos[1]])
            rects[Bishop(self.team, self.pos, self.game)] = self.pos_to_rect([self.pos[0] + 3, self.pos[1]])
            left = self.pos[1] * width
            top = (self.pos[0] + 4) * height
            cross_rect = pygame.Rect(left, top, width, height // 2)
            rects["cross"] = cross_rect
        else:
            rects[Queen(self.team, self.pos, self.game)] = self.pos_to_rect(self.pos)
            rects[Knight(self.team, self.pos, self.game)] = self.pos_to_rect([self.pos[0] - 1, self.pos[1]])
            rects[Rook(self.team, self.pos, self.game)] = self.pos_to_rect([self.pos[0] - 2, self.pos[1]])
            rects[Bishop(self.team, self.pos, self.game)] = self.pos_to_rect([self.pos[0] - 3, self.pos[1]])
            left = self.pos[1] * width
            top = (self.pos[0] - 3.5) * height
            cross_rect = pygame.Rect(left, top, width, height // 2)
            rects["cross"] = cross_rect

        return rects
