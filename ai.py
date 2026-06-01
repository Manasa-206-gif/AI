import random

# Piece-square tables for positional evaluation
PAWN_TABLE = [
    [ 0,  0,  0,  0,  0,  0,  0,  0],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [ 5,  5, 10, 25, 25, 10,  5,  5],
    [ 0,  0,  0, 20, 20,  0,  0,  0],
    [ 5, -5,-10,  0,  0,-10, -5,  5],
    [ 5, 10, 10,-20,-20, 10, 10,  5],
    [ 0,  0,  0,  0,  0,  0,  0,  0],
]

KNIGHT_TABLE = [
    [-50,-40,-30,-30,-30,-30,-40,-50],
    [-40,-20,  0,  0,  0,  0,-20,-40],
    [-30,  0, 10, 15, 15, 10,  0,-30],
    [-30,  5, 15, 20, 20, 15,  5,-30],
    [-30,  0, 15, 20, 20, 15,  0,-30],
    [-30,  5, 10, 15, 15, 10,  5,-30],
    [-40,-20,  0,  5,  5,  0,-20,-40],
    [-50,-40,-30,-30,-30,-30,-40,-50],
]

BISHOP_TABLE = [
    [-20,-10,-10,-10,-10,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5, 10, 10,  5,  0,-10],
    [-10,  5,  5, 10, 10,  5,  5,-10],
    [-10,  0, 10, 10, 10, 10,  0,-10],
    [-10, 10, 10, 10, 10, 10, 10,-10],
    [-10,  5,  0,  0,  0,  0,  5,-10],
    [-20,-10,-10,-10,-10,-10,-10,-20],
]

ROOK_TABLE = [
    [ 0,  0,  0,  0,  0,  0,  0,  0],
    [ 5, 10, 10, 10, 10, 10, 10,  5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [ 0,  0,  0,  5,  5,  0,  0,  0],
]

QUEEN_TABLE = [
    [-20,-10,-10, -5, -5,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5,  5,  5,  5,  0,-10],
    [ -5,  0,  5,  5,  5,  5,  0, -5],
    [  0,  0,  5,  5,  5,  5,  0, -5],
    [-10,  5,  5,  5,  5,  5,  0,-10],
    [-10,  0,  5,  0,  0,  0,  0,-10],
    [-20,-10,-10, -5, -5,-10,-10,-20],
]

KING_TABLE = [
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-20,-30,-30,-40,-40,-30,-30,-20],
    [-10,-20,-20,-20,-20,-20,-20,-10],
    [ 20, 20,  0,  0,  0,  0, 20, 20],
    [ 20, 30, 10,  0,  0, 10, 30, 20],
]

PIECE_TABLES = {
    'Pawn':   PAWN_TABLE,
    'Knight': KNIGHT_TABLE,
    'Bishop': BISHOP_TABLE,
    'Rook':   ROOK_TABLE,
    'Queen':  QUEEN_TABLE,
    'King':   KING_TABLE,
}

PIECE_VALUES = {
    'Pawn': 100, 'Knight': 320, 'Bishop': 330,
    'Rook': 500, 'Queen': 900, 'King': 20000
}


def evaluate(board):
    score = 0
    for r in range(8):
        for c in range(8):
            p = board.grid[r][c]
            if p is None:
                continue
            name = p.__class__.__name__
            val = PIECE_VALUES.get(name, 0)
            table = PIECE_TABLES.get(name, None)
            if table:
                pos_val = table[r][c] if p.color == 'black' else table[7 - r][c]
            else:
                pos_val = 0
            if p.color == 'black':
                score += val + pos_val
            else:
                score -= val + pos_val
    return score


def minimax(board, depth, alpha, beta, maximizing):
    if depth == 0:
        return evaluate(board), None

    color = 'black' if maximizing else 'white'
    all_moves = board.get_all_moves(color)
    if not all_moves:
        return evaluate(board), None

    best_move = None

    if maximizing:
        max_eval = float('-inf')
        for from_pos, to_pos in all_moves:
            clone = board.clone()
            clone.move(from_pos, to_pos)
            clone.check_promotion()
            eval_score, _ = minimax(clone, depth - 1, alpha, beta, False)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = (from_pos, to_pos)
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for from_pos, to_pos in all_moves:
            clone = board.clone()
            clone.move(from_pos, to_pos)
            clone.check_promotion()
            eval_score, _ = minimax(clone, depth - 1, alpha, beta, True)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = (from_pos, to_pos)
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move


def get_ai_move(board, depth=3):
    """Get the best move for black (AI) using minimax."""
    _, best = minimax(board, depth, float('-inf'), float('inf'), True)
    if best is None:
        moves = board.get_all_moves('black')
        if moves:
            return random.choice(moves)
    return best