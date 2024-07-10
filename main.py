import pygame
import sys

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
        #initialize game
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_heigth))
        pygame.display.set_caption("Chess")
        self.clock = pygame.time.Clock()
        self.counter = 0
        self.turn = 1
        self.last_selected = Piece("Default", "Default", (-1, -1), self)
        self.last_moved = None
        self.last_move_from = None
        self.last_move_to = None
        self.en_passant_move = None
        self.king_pos = None
        self.available_moves = []
        
        #initialize pieces
        self.piece_locations = [0] * 64
        self.initialize_pieces()
        
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
            self.checks()

    def checks(self):
        if self.counter < self.settings.counter:
            self.counter += 1
        else:
            self.counter = 0
    
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
            select = False
            collide_available_move = False
            mouse_pos = pygame.mouse.get_pos()
            clicked_idx = (mouse_pos[1] // 75) * 8 + (mouse_pos[0] // 75)
            self.last_selected.select = False
            for piece in filter(lambda piece: piece != 0, self.piece_locations):
                selected_piece_rect = pygame.Rect(piece.pos[1] * 75, piece.pos[0] * 75, 75, 75)

                if piece == self.last_selected or selected_piece_rect in self.last_selected.available_moves_rect:
                    for rect in self.last_selected.available_moves_rect:
                        if rect.collidepoint(mouse_pos):
                            self.last_selected.move(clicked_idx)
                            select = True
                            collide_available_move = True
                            break

                if selected_piece_rect.collidepoint(mouse_pos) and not collide_available_move:
                    self.collide_grid_select(piece)
                    select = True
                    break

            if not select:
                self.last_selected = Piece("Default", "Default", (-1, -1), self)

    def get_turn(self):
        return "white" if self.turn == 1 else "black"
    
    def is_king_in_check(self, team):
        king_pos = None

        # Find the king's position
        for piece in self.piece_locations:
            if piece != 0 and piece.name == "king" and piece.team == team:
                king_pos = piece.pos
                self.king_pos = piece.idx
                break

        if not king_pos:
            raise ValueError(f"No King found for the {team} team.")

        # Generate all opponent moves
        opponent_team = "white" if team == "black" else "black"
        opponent_moves = []

        for piece in self.piece_locations:
            if piece != 0 and piece.team == opponent_team:
                if isinstance(piece, Pawn):
                    piece.enable_en_passant = False
                opponent_moves.extend(piece.available_moves(self.piece_locations))
                piece.enable_en_passant = True

        # Check if any opponent move can capture the King
        for move in opponent_moves:
            if move == king_pos:
                return True

        return False

    def collide_grid_select(self, piece):
        if self.get_turn() != piece.team: return

        piece.select = True
        self.select = True
        self.last_selected = piece
        self.available_moves = piece.available_moves(self.piece_locations)


    def update_screen(self):
        pygame.display.flip()
        self.draw_bg()
        self.draw_pieces()
        self.clock.tick(self.settings.FPS)

    def draw_bg(self):
        W_COLOR = self.settings.white_bg_color
        B_COLOR = self.settings.black_bg_color
        width = self.settings.screen_heigth / 8
        height = self.settings.screen_width / 8

        for row in range(8):
            for col in range(8):
                color = B_COLOR if (row + col) % 2 == 0 else W_COLOR
                pygame.draw.rect(self.screen, color, (col * width, row * height, width, height))

    def draw_pieces(self):
        for piece in self.piece_locations:
            if piece == 0 or piece == None:
                continue
            
            if piece.select:
                piece.draw_select()
                piece.draw_available_moves(self.available_moves)

            if self.is_king_in_check(self.get_turn()):
                if self.counter < (self.settings.counter / 2):
                    self.piece_locations[self.king_pos].draw_check()
            piece.draw_piece()

if __name__ == '__main__':
    chess = Chess()
    chess.main()