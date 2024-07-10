import pygame
import sys

from settings import Settings
from piece import Piece
from pawn import Pawn
from rook import Rook
from bishop import Bishop
from king import King
from knight import Knight
from queen import Queen#

# TO DO
# 1. Available Moves when in check
# 3. Unhardcode small image
# 4. Unhardcode font size
# 5. Unhardcode (marges) side screen
# 6. Add winner code
# 7. Add Forfeit code
# 8. Add Pawn promotion code

# Hard Bonus Ai

class Chess:
    def __init__(self):
        #initialize game
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width + self.settings.screen_width_side_screen, self.settings.screen_heigth + self.settings.screen_height_side_screen))
        pygame.display.set_caption("Chess")
        self.clock = pygame.time.Clock()
        self.counter = 0
        self.turn = 1
        self.last_selected = Piece("Default", "Default", (-1, -1), self)
        self.last_moved = None
        self.last_move_from = None
        self.last_move_to = None
        self.en_passant_move = None
        self.king_white = None
        self.king_black = None
        self.select = False
        self.taken_pieces = []
        self.playing = True
        self.winner = None
        
        #initialize pieces
        self.piece_locations = [0] * 64
        self.initialize_pieces()

        for piece in filter(lambda piece: piece != 0, self.piece_locations):
            if piece.name == "king":
                if piece.team == "white":
                    self.king_white = piece
                else:
                    self.king_black = piece
        
        #initialize grid
        self.grid_cells = []
        self.initialize_grid()

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
            self.check_events()
            self.update_screen()
        
    
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Quit the game
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.check_event_mousedown(event)

            elif event.type == pygame.KEYDOWN:
                print(self.en_passant_move)

    def check_event_mousedown(self, event):
        if event.button == 1:  # Left mouse button
            mouse_pos = pygame.mouse.get_pos()
            
            if(mouse_pos[0] < self.settings.screen_width and mouse_pos[1] < self.settings.screen_heigth):
                self.check_chess_board(mouse_pos)
                self.is_king_in_check()
            else:
                self.check_side_board(mouse_pos)

    def check_chess_board(self, mouse_pos):
        width = self.settings.screen_width / 8
        height = self.settings.screen_heigth / 8
        select = False
        collide_available_move = False
        clicked_idx = (mouse_pos[1] // width) * 8 + (mouse_pos[0] // height)
        self.last_selected.select = False
        for piece in filter(lambda piece: piece != 0, self.piece_locations):
            piece.get_available_moves()
            selected_piece_rect = pygame.Rect(piece.pos[1] * width, piece.pos[0] * height, width, height)

            if piece == self.last_selected or selected_piece_rect in self.last_selected.available_moves_rect:
                for rect in self.last_selected.available_moves_rect:
                    if rect.collidepoint(mouse_pos):
                        self.last_selected.move(int(clicked_idx))
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
        
    def check_side_board(self, mouse_pos):
        under_right_border_rect = pygame.Rect(self.settings.screen_width, self.settings.screen_heigth,
                                self.settings.screen_width_side_screen, self.settings.screen_height_side_screen)
        if under_right_border_rect.collidepoint(mouse_pos):
            # FORFEIT
            print("FORFEIT")
            pass

    def get_turn(self):
        return "white" if self.turn == 1 else "black"
    
    def is_king_in_check(self):
        white_moves = []
        black_moves = []
        self.king_white.in_check = False
        self.king_black.in_check = False

        for piece in filter(lambda piece: piece != 0, self.piece_locations):
            if piece.name == "king":
                if piece.team == "white":
                    self.king_white = piece
                else:
                    self.king_black = piece

            if piece.team == "white":
                white_moves.extend(piece.available_moves)
            else:
                black_moves.extend(piece.available_moves)

        for move in white_moves:
            if move == self.king_black.pos:
                self.king_white.in_check = True
            
        for move in black_moves:
            if move == self.king_white.pos:
                self.king_black.in_check = True

    def collide_grid_select(self, piece):
        if self.get_turn() != piece.team: return

        self.select = True
        piece.select = True
        self.last_selected = piece


    def update_screen(self):
        pygame.display.flip()
        self.clock.tick(self.settings.FPS)
        self.draw_bg()
        self.draw_pieces()
        self.draw_side_screen()

        self.counter = self.counter + 1 if self.counter < self.settings.counter else 0

    def draw_bg(self):
        W_COLOR = self.settings.white_bg_color
        B_COLOR = self.settings.black_bg_color
        width = self.settings.screen_heigth / 8
        height = self.settings.screen_width / 8
        self.screen.fill(self.settings.bg_color)

        for row in range(8):
            for col in range(8):
                color = B_COLOR if (row + col) % 2 == 0 else W_COLOR
                pygame.draw.rect(self.screen, color, (col * width, row * height, width, height))

    def draw_pieces(self):
        for piece in self.piece_locations:
            if piece == 0 or piece == None: continue
            
            if piece.select:
                piece.draw_select()
                piece.draw_available_moves()
            
            piece.draw_piece()
            if piece.name != "king": continue
            if piece.in_check:
                if self.counter < (self.settings.counter / 2):
                    self.piece_locations[self.king_black.idx if piece.team == "white" else self.king_white.idx].draw_check()
        
    def draw_side_screen(self):
        self.draw_forfeit()
        self.draw_piece_to_move()
        self.draw_taken_pieces()

    def draw_forfeit(self):
        under_right_border_rect = pygame.Rect(self.settings.screen_width, self.settings.screen_heigth,
                            self.settings.screen_width_side_screen, self.settings.screen_height_side_screen)
        pygame.draw.rect(self.screen, self.settings.under_right_border_color, under_right_border_rect)
        text_forfeit_surface = self.settings.forfeit_font.render("FORFEIT", True, "black")
        text_forfeit_rect = text_forfeit_surface.get_rect()
        text_forfeit_x = under_right_border_rect.x + (under_right_border_rect.width - text_forfeit_rect.width) / 2
        text_forfeit_y = under_right_border_rect.y + (under_right_border_rect.height - text_forfeit_rect.height) / 2
        self.screen.blit(text_forfeit_surface, (text_forfeit_x, text_forfeit_y))

    def draw_piece_to_move(self):
        under_border_rect = pygame.Rect(0, self.settings.screen_heigth, 
                            self.settings.screen_width, self.settings.screen_height_side_screen)
        pygame.draw.rect(self.screen, self.settings.under_border_color, under_border_rect)
        end_string_turn = "piece to move" if not self.select else "destination"
        text_turn_surface = self.settings.turn_font.render(f"{self.get_turn().capitalize()}: Select a {end_string_turn}!", True, "black")
        text_turn_rect = text_turn_surface.get_rect()
        text_turn_rect_x = under_border_rect.x + 10
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
                self.screen.blit(piece.img_small, (self.settings.screen_width + 25, 5 + 50 * black))
                black += 1
            else:
                self.screen.blit(piece.img_small, (self.settings.screen_width + 125, 5 + 50 * white))
                white += 1


if __name__ == '__main__':
    chess = Chess()
    chess.main()