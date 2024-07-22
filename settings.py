import pygame

class Settings:
    def __init__(self):
        self.screen_width = 600
        self.screen_heigth = 600
        self.screen_width_side_screen = 200
        self.screen_height_side_screen = 200

        self.bg_color = "#D6D4A0"
        self.FPS = 60

        self.right_border_color = "#664147"
        self.under_border_color = "#2F9C95"
        self.under_right_border_color = "#565264"

        self.forfeit_font = pygame.font.Font('freesansbold.ttf', 36)
        self.turn_font = pygame.font.Font('freesansbold.ttf', 36)

        self.white_bg_color = (118,150,86)
        self.black_bg_color = (255,255,255)
        self.select_bg_color = (50, 50, 50)
        self.available_move_bg_color = (100, 100, 100)

        self.winner_bg_color = (0, 0, 0)
        self.winner_scale = 1.5
        self.winner_font = pygame.font.Font('freesansbold.ttf', 36)
        self.winner_text_color = (255, 255, 255)

        self.promotion_bg_color = (30, 30, 30)
        self.promotion_cross_color = (255, 0, 0)
        self.promotion_cross_thickness = 3

        self.counter = 30
        self.checking_color = "dark red"
        self.checking_thickness = 5