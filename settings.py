import pygame
from pygame import mixer

class Settings:
    def __init__(self):
        pygame.init()
        mixer.init()
        self.capture_sound = mixer.Sound("sound/capture.mp3")
        self.castle_sound = mixer.Sound("sound/castle.mp3")
        self.check_sound = mixer.Sound("sound/check.mp3")
        self.end_sound = mixer.Sound("sound/end.mp3")
        self.move_sound = mixer.Sound("sound/move.mp3")
        self.promote_sound = mixer.Sound("sound/promote.mp3")
        self.start_sound = mixer.Sound("sound/start.mp3")
        self.tenseconds_sound = mixer.Sound("sound/tenseconds.mp3")

        self.screen_width = 600
        self.screen_heigth = 600
        self.screen_width_side_screen = 200
        self.screen_height_side_screen = 200
        self.fontsize = int((self.screen_width + self.screen_width_side_screen) // 22.2)

        self.bg_color = "#D6D4A0"
        self.FPS = 60

        self.right_border_color = "#664147"
        self.under_border_color = "#2F9C95"
        self.under_right_border_color = "#565264"

        self.forfeit_font = pygame.font.Font('freesansbold.ttf', self.fontsize)
        self.forfeit_font_color = (0, 0, 0)
        self.turn_font = pygame.font.Font('freesansbold.ttf', self.fontsize)
        self.turn_font_color = (0, 0, 0)

        self.white_bg_color = (118,150,86)
        self.black_bg_color = (255,255,255)
        self.select_bg_color = (50, 50, 50)
        self.available_move_bg_color = (100, 100, 100)

        self.winner_bg_color = (0, 0, 0)
        self.winner_scale = 1.5
        self.winner_font = pygame.font.Font('freesansbold.ttf', self.fontsize)
        self.winner_text_color = (255, 255, 255)

        self.promotion_bg_color = (30, 30, 30)
        self.promotion_cross_color = (255, 0, 0)
        self.promotion_cross_thickness = 3

        self.counter = 30
        self.checking_color = (255, 0, 0)
        self.checking_thickness = 5

        self.timer = 300
        self.timer_bg_color = (255, 0, 0)
        self.timer_white_color = (255, 255, 255)
        self.timer_black_color = (0, 0, 0)
        self.timer_font = pygame.font.Font('freesansbold.ttf', self.fontsize)
