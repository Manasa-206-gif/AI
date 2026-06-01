import copy
from pieces import Pawn, Rook, Knight, Bishop, Queen, King


class Board:
    def __init__(self):
        self.grid = [[None] * 8 for _ in range(8)]
        self._setup()

    def _setup(self):
        order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for col, PieceClass in enumerate(order):
            self.grid[0][col] = PieceClass('black')
            self.grid[7][col] = PieceClass('white')
        for col in range(8):
            self.grid[1][col] = Pawn('black')
            self.grid[6][col] = Pawn('white')

    def move(self, from_pos, to_pos):
        r1, c1 = from_pos
        r2, c2 = to_pos
        captured = self.grid[r2][c2]
        self.grid[r2][c2] = self.grid[r1][c1]
        self.grid[r1][c1] = None
        return captured

    def clone(self):
        new_board = Board.__new__(Board)
        new_board.grid = [[None] * 8 for _ in range(8)]
        for r in range(8):
            for c in range(8):
                p = self.grid[r][c]
                if p:
                    new_board.grid[r][c] = p.__class__(p.color)
        return new_board

    def get_all_moves(self, color):
        moves = []
        for r in range(8):
            for c in range(8):
                p = self.grid[r][c]
                if p and p.color == color:
                    for move in p.get_moves(r, c, self.grid):
                        moves.append(((r, c), move))
        return moves

    def find_king(self, color):
        for r in range(8):
            for c in range(8):
                p = self.grid[r][c]
                if p and p.__class__.__name__ == 'King' and p.color == color:
                    return (r, c)
        return None

    def is_in_check(self, color):
        king_pos = self.find_king(color)
        if not king_pos:
            return False
        opponent = 'black' if color == 'white' else 'white'
        for r in range(8):
            for c in range(8):
                p = self.grid[r][c]
                if p and p.color == opponent:
                    if king_pos in p.get_moves(r, c, self.grid):
                        return True
        return False

    def check_promotion(self):
        promoted = []
        for col in range(8):
            p = self.grid[0][col]
            if p and p.__class__.__name__ == 'Pawn' and p.color == 'white':
                self.grid[0][col] = Queen('white')
                promoted.append((0, col))
            p = self.grid[7][col]
            if p and p.__class__.__name__ == 'Pawn' and p.color == 'black':
                self.grid[7][col] = Queen('black')
                promoted.append((7, col))
        return promoted