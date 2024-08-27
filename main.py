import pygame
import sys
import time
from settings import Settings
from piece import Piece
from pawn import Pawn
from rook import Rook
from bishop import Bishop
from king import King
from knight import Knight
from queen import Queen

class Chess:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width + self.settings.screen_width_side_screen, self.settings.screen_heigth + self.settings.screen_height_side_screen))
        pygame.display.set_caption("Chess")
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.counter = 0
        self.turn = 1
        self.last_selected = Piece("Default", "Default", (-1, -1), self)
        self.last_moved = None
        self.last_move_from = None
        self.last_move_to = None
        self.black_moves = []
        self.white_moves = []
        self.king_white = None
        self.king_black = None
        self.promotion = None
        self.check = None
        self.select = False
        self.piece_select = None
        self.taken_pieces = []
        self.playing = True
        self.winner = None
        self.piece_locations = [0] * 64
        self.legal_moves_white = []
        self.legal_moves_black = []
        self.moves_count = 0
        self.initialize_pieces()
        self.settings.start_sound.play()

        self.white_timer = self.settings.timer
        self.black_timer = self.settings.timer
        self.turn_start_time = time.time()
        self.play_ending_sound_once = True
        self.play_low_count_sound_white_once = True
        self.play_low_count_sound_black_once = True

        for piece in filter(lambda piece: piece != 0, self.piece_locations):
            if piece.name == "king":
                if piece.team == "white":
                    self.king_white = piece
                else:
                    self.king_black = piece
        
        self.grid_cells = []
        self.initialize_grid()

        self.board_history = [self.piece_locations[:]]
        self.repeat_moves_count = 0

    def test(self):
        self.piece_locations = [0] * 64
        piece = self.get_piece_class("king")("white", [0, 0], self)
        self.piece_locations[0] = piece

        piece = self.get_piece_class("king")("black", [7, 7], self)
        self.piece_locations[63] = piece

        piece = self.get_piece_class("knight")("white", [0, 1], self)
        self.piece_locations[1] = piece

    def initialize_grid(self):
        width = self.settings.screen_width / 8
        height = self.settings.screen_heigth / 8
        for row in range(8):
            for col in range(8):
                self.grid_cells.append(pygame.Rect(col * width, row * height, width, height))

    def initialize_pieces(self):
        for i in range(8):
            piece = self.get_piece_class("pawn")("black", [1, i], self)
            self.piece_locations[8 + i] = piece
        for i in range(8):
            piece = self.get_piece_class("pawn")("white", [6, i], self)
            self.piece_locations[48 + i] = piece
        piece_order = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]
        for col, piece_name in enumerate(piece_order):
            piece = self.get_piece_class(piece_name)("white", [7, col], self)
            self.piece_locations[56 + col] = piece
            piece = self.get_piece_class(piece_name)("black", [0, col], self)
            self.piece_locations[0 + col] = piece

    def get_piece_class(self, piece):
        piece_classes = {
            "pawn": Pawn,
            "rook": Rook,
            "bishop": Bishop,
            "queen": Queen,
            "king": King,
            "knight": Knight
        }
        piece_class = piece_classes.get(piece)
        return piece_class

    def main(self):
        while(True):
            self.check_pieces()
            self.check_events()
            self.simulate_move()
            self.check_winner()
            self.check_draw()
            self.update_screen()
            
    def check_pieces(self):
        self.get_pieces_pos()
        self.king_black.in_check = self.is_king_in_check(self.king_white.team)
        self.king_white.in_check = self.is_king_in_check(self.king_black.team)

    def get_pieces_pos(self):
        for piece in filter(lambda piece: piece != 0 and piece.name in ["king", "pawn"], self.piece_locations):
            if piece.name == "king":
                if piece.team == "white":
                    self.king_white = piece
                else:
                    self.king_black = piece

                if piece.in_check:
                    if self.counter < (self.settings.counter / 2):
                        self.check = piece
            
            if piece.name == "pawn":
                if piece.pawn_promotion:
                    self.promotion = piece


    def is_king_in_check(self, team):
        if team == "white":
            for move in self.black_moves:
                if move == self.king_white.pos:
                    return True
        else:
            for move in self.white_moves:
                if move == self.king_black.pos:
                    return True
            
        return False
                
    def get_all_moves(self, team, piece_locations):
        moves = []
        for piece in filter(lambda piece: piece != 0 and piece.team == team, piece_locations):
            available_moves = piece.get_available_moves(piece_locations)
            moves.extend(available_moves)

        return moves
   
    def is_legal_move(self, piece_locations, team):
        all_black_moves = self.get_all_moves("black", piece_locations)
        all_white_moves = self.get_all_moves("white", piece_locations)

        if team == "black":
            if self.king_black.pos in all_white_moves:
                return False
        else:
            if self.king_white.pos in all_black_moves:
                return False
        return True

    def simulate_move(self):
        self.legal_moves_black = []
        self.legal_moves_white = []
        for piece in filter(lambda piece: piece != 0, self.piece_locations):
            piece_locations = self.piece_locations[:]
            old_pos = piece.pos
            old_idx = piece.idx
            piece_moves = []

            for move in piece.get_available_moves(piece_locations):
                piece.pos = move
                new_idx = piece.pos_to_idx(move)
                piece.idx = new_idx
                piece_locations[old_idx] = 0
                piece_locations[piece.idx] = piece
                piece_locations[piece.idx].change_available_moves(piece_locations[piece.idx].get_available_moves(piece_locations))
                if self.is_legal_move(piece_locations, piece.team):
                    piece_moves.append(move)
                piece_locations = self.piece_locations[:] 

            piece.pos = old_pos
            piece.idx = old_idx
            piece.change_available_moves(piece_moves)
            if piece_moves != []:
                if piece.team == "white":
                    self.legal_moves_white.append(piece_moves)
                else:
                    self.legal_moves_black.append(piece_moves)
            piece.make_rect()
            piece_locations = self.piece_locations

    def check_winner(self):
        if self.legal_moves_black == [] and self.king_white.in_check:
            self.winner = "white"
            if self.play_ending_sound_once: self.settings.check_sound.play()
        if self.legal_moves_white == [] and self.king_black.in_check:
            if self.play_ending_sound_once: self.settings.check_sound.play()
            self.winner = "black"

        self.check_time()

        if self.winner and self.play_ending_sound_once:
            self.playing = False
            self.play_ending_sound_once = False
            self.settings.end_sound.play()

    def check_draw(self):
        self.repeat_moves_count = -1
        for board in self.board_history:
            repeat = True
            for i in range(len(self.piece_locations)):
                if board[i] != self.piece_locations[i]:
                    repeat = False
                    break
            if repeat: self.repeat_moves_count += 1

        if self.repeat_moves_count == 2 or self.moves_count == 100:
            self.winner = "draw"

        if self.legal_moves_black == [] and not self.king_white.in_check:
            self.winner = "draw"
            if self.play_ending_sound_once: self.settings.check_sound.play()
        if self.legal_moves_white == [] and not self.king_black.in_check:
            if self.play_ending_sound_once: self.settings.check_sound.play()
            self.winner = "draw"

        black_pieces = []
        white_pieces = []
        for piece in filter(lambda piece: piece != 0, self.piece_locations):
            if piece.team == "white":
                white_pieces.append(piece)
            else:
                black_pieces.append(piece)
        if len(black_pieces) <= 2 and len(white_pieces) <= 2:
            black_insufficient = False
            white_insufficient = False
            for piece in black_pieces:
                if piece.name == "king":
                    black_insufficient = True
                    continue
                if piece.name == "knight" or piece.name == "bishop":
                    black_insufficient = True
                else:
                    black_insufficient = False
                    break
            for piece in white_pieces:
                if piece.name == "king":
                    white_insufficient = True
                    continue
                if piece.name == "knight" or piece.name == "bishop":
                    white_insufficient = True
                else:
                    white_insufficient = False
                    break
            if white_insufficient and black_insufficient:
                self.winner = "draw"

    def check_time(self):
        current_time = time.time()
        elapsed_time = current_time - self.turn_start_time
        self.turn_start_time = current_time
        if self.turn == 1:
            self.white_timer -= elapsed_time
            if self.white_timer <= 0:
                self.white_timer = 0
                self.winner = "black"
            
            if self.white_timer <= 10 and self.play_low_count_sound_white_once:
                self.play_low_count_sound_white_once = False
                self.settings.tenseconds_sound.play()
            
        else:
            self.black_timer -= elapsed_time
            if self.black_timer <= 0:
                self.black_timer = 0
                self.winner = "white"

            if self.black_timer <= 10 and self.play_low_count_sound_black_once:
                self.play_low_count_sound_black_once = False
                self.settings.tenseconds_sound.play()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.check_event_mousedown(event)

            elif event.type == pygame.KEYDOWN:
                self.test()

    def check_event_mousedown(self, event):
        if event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if not self.promotion:
                if(mouse_pos[0] < self.settings.screen_width and mouse_pos[1] < self.settings.screen_heigth):
                    self.check_chess_board(mouse_pos)
                else:
                    self.check_side_board(mouse_pos)
            else:
                self.check_promotion(mouse_pos)


    def check_chess_board(self, mouse_pos):
        width = self.settings.screen_width / 8
        height = self.settings.screen_heigth / 8
        select = False
        collide_available_move = False
        clicked_idx = (mouse_pos[1] // width) * 8 + (mouse_pos[0] // height)
        self.last_selected.select = False

        for piece in filter(lambda piece: piece != 0, self.piece_locations):
            selected_piece_rect = pygame.Rect(piece.pos[1] * width, piece.pos[0] * height, width, height)

            if piece == self.last_selected or selected_piece_rect in self.last_selected.available_moves_rect:
                for rect in self.last_selected.available_moves_rect:
                    if rect.collidepoint(mouse_pos):
                        self.last_selected.move(int(clicked_idx))
                        self.piece_select = None
                        self.select = False
                        select = True
                        collide_available_move = True
                        break

            if selected_piece_rect.collidepoint(mouse_pos) and not collide_available_move:
                self.collide_grid_select(piece)
                select = True
                break

        if not select:
                self.last_selected = Piece("Default", "Default", (-1, -1), self)
                self.select = False
                self.piece_select = None
        
    def check_side_board(self, mouse_pos):
        under_right_border_rect = pygame.Rect(self.settings.screen_width, self.settings.screen_heigth,
                                self.settings.screen_width_side_screen, self.settings.screen_height_side_screen)
        if under_right_border_rect.collidepoint(mouse_pos):
            print("FORFEIT")
            pass

    def check_promotion(self, mouse_pos):
        promotion_rects = self.promotion.get_promotion_rect()
        for rect in promotion_rects:
            if rect == "cross" and promotion_rects["cross"].collidepoint(mouse_pos):
                self.promotion = None
                self.last_moved.pos = self.last_move_from
                self.last_moved.idx = Piece.pos_to_idx(self, self.last_move_from)
                self.last_moved.pawn_promotion = False
                self.piece_locations[self.last_moved.idx] = self.last_moved
                self.piece_locations[Piece.pos_to_idx(self, self.last_move_to)] = 0 
                if not self.last_moved.piece_taken:
                    self.piece_locations[Piece.pos_to_idx(self, self.last_move_to)] = 0
                else:
                    self.piece_locations[Piece.pos_to_idx(self, self.last_move_to)] = self.taken_pieces[-1]
                    self.taken_pieces.pop()
                break

            if promotion_rects[rect].collidepoint(mouse_pos):
                self.turn *= -1
                self.piece_locations[self.promotion.idx] = rect
                self.promotion = None
                self.settings.promote_sound.play()

    def get_turn(self):
        return "white" if self.turn == 1 else "black"

    def collide_grid_select(self, piece):
        if self.get_turn() != piece.team: return

        self.select = True
        self.piece_select = piece
        self.last_selected = piece

    def update_screen(self):
        pygame.display.flip()
        self.clock.tick(self.settings.FPS)
        self.draw_bg()
        self.draw_pieces()
        self.draw_side_screen()
        self.draw_winner()

        self.counter = self.counter + 1 if self.counter < self.settings.counter else 0

    def draw_bg(self):
        W_COLOR = self.settings.white_bg_color
        B_COLOR = self.settings.black_bg_color
        width = self.settings.screen_heigth // 8
        height = self.settings.screen_width // 8
        self.screen.fill(self.settings.bg_color)

        for row in range(8):
            for col in range(8):
                color = B_COLOR if (row + col) % 2 == 0 else W_COLOR
                pygame.draw.rect(self.screen, color, (col * width, row * height, width, height))

    def draw_pieces(self):
        if self.piece_select:
            self.piece_select.draw_select()
            self.piece_select.draw_available_moves()

        for piece in self.piece_locations:
            if piece == 0 or piece == None: continue
            piece.draw_piece()
        
        if self.check:
            self.piece_locations[self.king_black.idx if self.check.team == "white" else self.king_white.idx].draw_check()
            self.check = None

        if self.promotion:
            self.promotion.draw_promotion()
            self.promotion = None
        
    def draw_side_screen(self):
        self.draw_forfeit()
        self.draw_piece_to_move()
        self.draw_taken_pieces()
        self.draw_timer()

    def draw_timer(self):
        timer_border_rect = pygame.Rect(self.settings.screen_width // 5, self.settings.screen_heigth,
                                        self.settings.screen_width - (self.settings.screen_width // 5 * 2), self.settings.screen_height_side_screen // 3.5)
        pygame.draw.rect(self.screen, self.settings.timer_bg_color, timer_border_rect)

        white_minutes, white_seconds = divmod(int(self.white_timer), 60)
        black_minutes, black_seconds = divmod(int(self.black_timer), 60)
        white_time_str = f"{white_minutes}:{white_seconds:02}"
        black_time_str = f"{black_minutes}:{black_seconds:02}"

        text_timer_black_surface = self.settings.timer_font.render(black_time_str, True, self.settings.timer_black_color)
        text_timer_black_rect = text_timer_black_surface.get_rect()
        text_timer_black_x = timer_border_rect.x + timer_border_rect.width - text_timer_black_rect.width - (text_timer_black_rect.width // 14.4)
        text_timer_black_y = timer_border_rect.y + (text_timer_black_rect.height // 3)
        self.screen.blit(text_timer_black_surface, (text_timer_black_x, text_timer_black_y))

        text_timer_white_surface = self.settings.timer_font.render(white_time_str, True, self.settings.timer_white_color)
        text_timer_white_rect = text_timer_white_surface.get_rect()
        text_timer_white_x = timer_border_rect.x + (text_timer_white_rect.width // 14.4)
        text_timer_white_y = timer_border_rect.y + (text_timer_white_rect.height // 3)
        self.screen.blit(text_timer_white_surface, (text_timer_white_x, text_timer_white_y))


    def draw_forfeit(self):
        under_right_border_rect = pygame.Rect(self.settings.screen_width, self.settings.screen_heigth,
                            self.settings.screen_width_side_screen, self.settings.screen_height_side_screen)
        pygame.draw.rect(self.screen, self.settings.under_right_border_color, under_right_border_rect)
        text_forfeit_surface = self.settings.forfeit_font.render("FORFEIT", True, self.settings.forfeit_font_color)
        text_forfeit_rect = text_forfeit_surface.get_rect()
        text_forfeit_x = under_right_border_rect.x + (under_right_border_rect.width - text_forfeit_rect.width) / 2
        text_forfeit_y = under_right_border_rect.y + (under_right_border_rect.height - text_forfeit_rect.height) / 2
        self.screen.blit(text_forfeit_surface, (text_forfeit_x, text_forfeit_y))

    def draw_piece_to_move(self):
        under_border_rect = pygame.Rect(0, self.settings.screen_heigth, 
                            self.settings.screen_width, self.settings.screen_height_side_screen)
        pygame.draw.rect(self.screen, self.settings.under_border_color, under_border_rect)
        end_string_turn = "piece to move" if not self.select else "destination"
        text_turn_surface = self.settings.turn_font.render(f"{self.get_turn().capitalize()}: Select a {end_string_turn}!", True, self.settings.turn_font_color)
        text_turn_rect = text_turn_surface.get_rect()
        text_turn_rect_x = under_border_rect.x + (self.settings.screen_width // 60)
        text_turn_rect_y = under_border_rect.y  + (under_border_rect.height - text_turn_rect.height) / 2
        self.screen.blit(text_turn_surface, (text_turn_rect_x, text_turn_rect_y))

    def draw_taken_pieces(self):
        right_border_rect = pygame.Rect(self.settings.screen_width, 0,
                        self.settings.screen_width_side_screen, self.settings.screen_heigth)
        pygame.draw.rect(self.screen, self.settings.right_border_color, right_border_rect)
        white = 0
        black = 0

        for piece in self.taken_pieces:
            if piece.team == "black":
                self.screen.blit(piece.img_small, (self.settings.screen_width + self.settings.screen_width_side_screen // 8,
                                                    (self.settings.screen_heigth // 120) + (self.settings.screen_heigth // 12) * black))
                black += 1
            else:
                self.screen.blit(piece.img_small, (self.settings.screen_width + self.settings.screen_width_side_screen // 1.6,
                                                    (self.settings.screen_heigth // 120) + (self.settings.screen_heigth // 12) * white))
                white += 1

    def draw_winner(self):
        if self.winner == None: return
        height = self.settings.screen_heigth
        width = self.settings.screen_width
        rect_height = height // self.settings.winner_scale
        rect_width = width // self.settings.winner_scale
        rect_x = (width - rect_width) // self.settings.winner_scale
        rect_y = (height - rect_height) // self.settings.winner_scale
        winner_bg_color = self.settings.winner_bg_color
        winner_rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
        pygame.draw.rect(self.screen, winner_bg_color, winner_rect)

        text = "winner " + self.winner if self.winner != "draw" else "draw"
        text_surface = self.settings.winner_font.render(text, True, self.settings.winner_text_color)
        text_rect = text_surface.get_rect(center=(rect_x + rect_width // 2, rect_y + rect_height // 2))
        self.screen.blit(text_surface, text_rect)

if __name__ == '__main__':
    chess = Chess()
    chess.main()