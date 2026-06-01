def on_board(r, c):
    return 0 <= r < 8 and 0 <= c < 8


def slide(row, col, board, directions):
    moves = []
    for dr, dc in directions:
        r, c = row + dr, col + dc
        while on_board(r, c):
            if board[r][c] is None:
                moves.append((r, c))
            else:
                if board[r][c].color != board[row][col].color:
                    moves.append((r, c))
                break
            r += dr
            c += dc
    return moves


class Piece:
    def __init__(self, color):
        self.color = color
        self.symbol = ''
        self.value = 0

    def get_moves(self, row, col, board):
        return []

    def copy(self):
        return self.__class__(self.color)


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '♟' if color == 'black' else '♙'
        self.value = 1

    def get_moves(self, row, col, board):
        moves = []
        d = -1 if self.color == 'white' else 1
        start = 6 if self.color == 'white' else 1

        if on_board(row + d, col) and board[row + d][col] is None:
            moves.append((row + d, col))
            if row == start and board[row + 2 * d][col] is None:
                moves.append((row + 2 * d, col))

        for dc in [-1, 1]:
            if on_board(row + d, col + dc):
                target = board[row + d][col + dc]
                if target and target.color != self.color:
                    moves.append((row + d, col + dc))
        return moves


class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '♜' if color == 'black' else '♖'
        self.value = 5

    def get_moves(self, row, col, board):
        return slide(row, col, board, [(1, 0), (-1, 0), (0, 1), (0, -1)])


class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '♞' if color == 'black' else '♘'
        self.value = 3

    def get_moves(self, row, col, board):
        moves = []
        for dr, dc in [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                       (1, -2), (1, 2), (2, -1), (2, 1)]:
            r, c = row + dr, col + dc
            if on_board(r, c):
                if board[r][c] is None or board[r][c].color != self.color:
                    moves.append((r, c))
        return moves


class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '♝' if color == 'black' else '♗'
        self.value = 3

    def get_moves(self, row, col, board):
        return slide(row, col, board, [(1, 1), (1, -1), (-1, 1), (-1, -1)])


class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '♛' if color == 'black' else '♕'
        self.value = 9

    def get_moves(self, row, col, board):
        return slide(row, col, board,
                     [(1, 0), (-1, 0), (0, 1), (0, -1),
                      (1, 1), (1, -1), (-1, 1), (-1, -1)])


class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '♚' if color == 'black' else '♔'
        self.value = 1000

    def get_moves(self, row, col, board):
        moves = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if on_board(r, c):
                    if board[r][c] is None or board[r][c].color != self.color:
                        moves.append((r, c))
        return moves