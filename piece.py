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
        self.path = f"chess/img/{name}_{'w' if team == 'white' else 'b'}.svg"
        self.select = False
        self.idx = pos[0] * 8 + pos[1]
        self.available_moves_rect = []

        self.grid_width = self.settings.screen_width / 8
        self.grid_height = self.settings.screen_heigth / 8

    def draw_piece(self):
        img = pygame.image.load(self.path)
        img = pygame.transform.scale(img, (self.grid_width / 1.5, self.grid_height / 1.5))

        # get the coordinates of the position, instead of the grid index
        pos = [self.pos[0] * self.grid_height, self.pos[1] * self.grid_width]
                
        # center piece
        x = pos[1] + (self.grid_height - img.get_height()) // 2
        y = pos[0] + (self.grid_width - img.get_width()) // 2

        #draw piece
        self.screen.blit(img, (x, y))

    def draw_select(self):
        pos = [self.pos[0] * self.grid_height, self.pos[1] * self.grid_width]
        dark_circle_radius = min(self.grid_width, self.grid_height) // 3
        center_x = pos[1] +self.grid_width // 2
        center_y = pos[0] + self.grid_height // 2
        pygame.draw.circle(self.screen, self.settings.select_bg_color, (center_x, center_y), dark_circle_radius)

    def draw_available_moves(self, available_moves):
        if available_moves == None: return
        for i in available_moves:
            pos = [i[0] * self.grid_height, i[1] * self.grid_width]
            dark_circle_radius = min(self.grid_width, self.grid_height) // 3
            center_x = pos[1] + self.grid_width // 2
            center_y = pos[0] + self.grid_height // 2
            pygame.draw.circle(self.screen, self.settings.available_move_bg_color, (center_x, center_y), dark_circle_radius)

    def index_to_pos(self, index):
        row = index // 8
        col = index % 8
        return [row, col]
    
    def available_moves(self, piece_locations):
        return [[-1, -1]]
    
    def move(self, clicked_idx):
        self.game.last_move_from = self.pos
        self.pos = self.index_to_pos(clicked_idx)
        self.game.last_move_to = self.pos
        self.game.piece_locations[self.idx] = 0
        self.idx = clicked_idx
        self.game.piece_locations[clicked_idx] = self
        self.game.last_moved = self
        self.available_moves_rect = []
        self.game.turn *= -1
        self.game.available_moves = None
        self.game.last_selected = Piece("Default", "Default", (-1, -1), self)