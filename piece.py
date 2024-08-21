import pygame
from settings import Settings

class Piece:
    def __init__(self, name, team, pos, game):
        self.game = game
        self.settings = Settings()
        self.screen = game.screen
        self.name = name
        self.team = team
        self.pos = pos
        self.grid_width = self.settings.screen_width / 8
        self.grid_height = self.settings.screen_heigth / 8
        if(self.name == "knight"):
            self.path = f"img/banaan_{'w' if team == "white" else 'b'}.png"
        else:
            self.path = f"img/{name}_{'w' if team == 'white' else 'b'}.svg"
        if self.name != "Default":
            self.img = pygame.image.load(self.path)
            self.img_small = pygame.transform.scale(self.img, (45, 45))
            self.img = pygame.transform.scale(self.img, (self.grid_width / 1.5, self.grid_height / 1.5))
        self.idx = int(pos[0] * 8 + pos[1])
        self.available_moves_rect = []
        self.available_moves = []
        self.piece_taken = False

        self.grid_width = self.settings.screen_width / 8
        self.grid_height = self.settings.screen_heigth / 8

    def draw_piece(self):
        pos = [self.pos[0] * self.grid_height, self.pos[1] * self.grid_width]
                
        x = pos[1] + (self.grid_height - self.img.get_height()) // 2
        y = pos[0] + (self.grid_width - self.img.get_width()) // 2

        self.screen.blit(self.img, (x, y))

    def draw_select(self):
        pos = [self.pos[0] * self.grid_height, self.pos[1] * self.grid_width]
        dark_circle_radius = min(self.grid_width, self.grid_height) // 3
        center_x = pos[1] +self.grid_width // 2
        center_y = pos[0] + self.grid_height // 2
        pygame.draw.circle(self.screen, self.settings.select_bg_color, (center_x, center_y), dark_circle_radius)

    def draw_available_moves(self):
        if self.available_moves == None: return
        for i in self.available_moves:
            pos = [i[0] * self.grid_height, i[1] * self.grid_width]
            dark_circle_radius = min(self.grid_width, self.grid_height) // 3
            center_x = pos[1] + self.grid_width // 2
            center_y = pos[0] + self.grid_height // 2
            pygame.draw.circle(self.screen, self.settings.available_move_bg_color, (center_x, center_y), dark_circle_radius)

    def index_to_pos(self, index):
        row = index // 8
        col = index % 8
        return [row, col]
    
    def pos_to_idx(self, pos):
        row, col = pos
        return row * 8 + col
    
    def get_available_moves(self):
        return [[-1, -1]]
    
    def change_available_moves(self, available_moves):
        self.available_moves = available_moves
    
    def make_rect(self):
        self.available_moves_rect = []
        for move in self.available_moves:
                self.available_moves_rect.append(self.pos_to_rect(move))

    def pos_to_rect(self, pos):
        width = self.game.settings.screen_width // 8
        height = self.game.settings.screen_heigth // 8
        return pygame.Rect(pos[1] * width, pos[0] * height, width, height)
    
    def move(self, clicked_idx):
        self.piece_taken = False
        self.game.last_move_from = self.pos
        self.pos = self.index_to_pos(clicked_idx)
        self.game.last_move_to = self.pos
        if self.game.piece_locations[clicked_idx] != 0:
            self.game.taken_pieces.append(self.game.piece_locations[clicked_idx])
            self.piece_taken = True
            self.settings.capture_sound.play()
            self.game.repeat_moves_count = 0
            self.game.board_history = []
        else:
            self.game.moves_count += 1
        self.game.piece_locations[self.idx] = 0
        self.idx = clicked_idx
        self.game.piece_locations[clicked_idx] = self
        self.game.last_moved = self
        self.available_moves_rect = []
        self.game.turn *= -1
        self.game.last_selected = Piece("Default", "Default", (-1, -1), self)
        self.game.board_history.append(self.game.piece_locations[:])

        self.settings.move_sound.play()