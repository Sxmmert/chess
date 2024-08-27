from piece import Piece

class Knight(Piece):
    def __init__(self, team, pos, game):
        super().__init__("knight", team, pos, game)

    def __repr__(self):
        return f"{self.team} knight at ({self.pos})"
    
    def __eq__(self, other):
        if isinstance(other, Knight):
            return self.team == other.team and self.name == other.name and self.pos == other.pos
        return False
    
    def __hash__(self):
        return hash(self.name)
    
    def get_available_moves(self, piece_locations):
        available_moves = []
        moves = [
            (-2, -1), (-2, 1), (2, -1), (2, 1),
            (-1, -2), (1, -2), (-1, 2), (1, 2)
        ]
        
        for move in moves:
            row, col = self.pos[0] + move[0], self.pos[1] + move[1]
            if 0 <= row < 8 and 0 <= col < 8:
                idx = row * 8 + col
                if piece_locations[idx] == 0 or piece_locations[idx].team != self.team:
                    available_moves.append([row, col])

        return available_moves
    
    def move(self, clicked_idx):
        super().move(clicked_idx)
        self.game.white_moves = self.game.get_all_moves("white", self.game.piece_locations)
        self.game.black_moves = self.game.get_all_moves("black", self.game.piece_locations)
        if self.game.is_king_in_check("white") or self.game.is_king_in_check("black"):
            self.settings.check_sound.play()