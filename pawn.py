from piece import Piece

class Pawn(Piece):
    def __init__(self, team, pos, game):
        super().__init__("pawn", team, pos, game)
        self.first_move = True
        self.en_passant = False

    def __repr__(self):
        return f"{self.team} pawn at ({self.pos})"
    
    def move(self, clicked_idx):
        super().move(clicked_idx)
        self.first_move = False
        if self.game.en_passant_move is not None:
            if self.pos == self.game.en_passant_move:
                if self.team == "white":
                    self.game.piece_locations[self.idx + 8] = 0
                else:
                    self.game.piece_locations[self.idx - 8] = 0
                self.game.en_passant_move = None


    def get_available_moves(self, en_passant_enabled = True):
        piece_locations = self.game.piece_locations
        self.available_moves_rect = []
        piece_location = int(self.pos[0] * 8 + self.pos[1])
        piece_step = -8 if self.team == "white" else 8
        self.en_passant = False
        en_passant_move = []
        available_moves = []

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
                    self.en_passant = True
                    
                if(self.pos[1] + 1 == self.game.last_move_to[1]):
                    if(self.team == "white"):
                        en_passant_move = [self.pos[0] - 1, self.pos[1] + 1]
                        available_moves.append(en_passant_move)
                    else:
                        en_passant_move = [self.pos[0] + 1, self.pos[1] + 1]
                        available_moves.append(en_passant_move)
                    self.en_passant = True

            self.game.en_passant_move = en_passant_move if self.en_passant else None

        self.available_moves = available_moves
        self.make_rect()
