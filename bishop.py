from piece import Piece

class Bishop(Piece):
    def __init__(self, team, pos, game):
        super().__init__("bishop", team, pos, game)

    def __repr__(self):
        return f"{self.team} bishop at ({self.pos})"
    
    def get_available_moves(self, piece_locations):
        available_moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for direction in directions:
            row, col = self.pos
            while 1:
                row += direction[0]
                col += direction[1]
                if 0 <= row < 8 and 0 <= col < 8:
                    idx = row * 8 + col
                    if piece_locations[idx] == 0:
                        available_moves.append([row, col])
                    else:
                        if piece_locations[idx].team != self.team:
                            available_moves.append([row, col])
                        break
                else:
                    break

        return available_moves
    
    def move(self, clicked_idx):
        super().move(clicked_idx)
        self.game.white_moves = self.game.get_all_moves("white", self.game.piece_locations)
        self.game.black_moves = self.game.get_all_moves("black", self.game.piece_locations)
        if self.game.is_king_in_check("white") or self.game.is_king_in_check("black"):
            self.settings.check_sound.play()