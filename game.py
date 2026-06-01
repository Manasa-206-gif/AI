import pygame
import threading
from board import Board
from ai import get_ai_move
from constants import *


class Game:
    def __init__(self, screen, mode=MODE_HVH, theme=None):
        self.screen      = screen
        self.mode        = mode
        self.board       = Board()
        self.selected    = None
        self.valid_moves = []
        self.turn        = 'white'
        self.game_over   = False
        self.winner      = None
        self.status_msg  = ""
        self.ai_thinking = False
        self.move_history      = []
        self._ai_move_result   = None

        if theme:
            self.light_sq   = theme[1]
            self.dark_sq    = theme[2]
            self.theme_name = theme[0]
        else:
            self.light_sq   = LIGHT_SQ
            self.dark_sq    = DARK_SQ
            self.theme_name = "Classic"

        self.piece_font = pygame.font.SysFont("segoeuisymbol", SQUARE_SIZE - 8)
        self.ui_font    = pygame.font.SysFont("arial", 18, bold=True)
        self.small_font = pygame.font.SysFont("arial", 14)

        self._update_status()

    # ── Helpers ───────────────────────────────────────────────
    def _legal_moves(self, row, col):
        piece = self.board.grid[row][col]
        if not piece:
            return []
        legal = []
        for move in piece.get_moves(row, col, self.board.grid):
            clone = self.board.clone()
            clone.move((row, col), move)
            if not clone.is_in_check(piece.color):
                legal.append(move)
        return legal

    def _has_any_legal_move(self, color):
        for r in range(8):
            for c in range(8):
                p = self.board.grid[r][c]
                if p and p.color == color:
                    if self._legal_moves(r, c):
                        return True
        return False

    def _update_status(self):
        if self.game_over:
            self.status_msg = f"{self.winner.upper()} WINS!" if self.winner else "STALEMATE!"
            return
        if self.mode == MODE_HVH:
            self.status_msg = f"{'WHITE' if self.turn=='white' else 'BLACK'}'s Turn"
        else:
            if self.turn == 'white':
                self.status_msg = "Your Turn  (You = White)"
            else:
                self.status_msg = "AI is thinking..." if self.ai_thinking else "AI's Turn"
        if self.board.is_in_check(self.turn):
            self.status_msg += "  ⚠ CHECK!"

    # ── Input ─────────────────────────────────────────────────
    def handle_click(self, mx, my):
        if self.game_over or self.ai_thinking:
            return
        if self.mode == MODE_HVA and self.turn == 'black':
            return

        bx = mx - OFFSET_X
        by = my - OFFSET_Y
        if not (0 <= bx < BOARD_SIZE and 0 <= by < BOARD_SIZE):
            return

        col   = bx // SQUARE_SIZE
        row   = by // SQUARE_SIZE
        piece = self.board.grid[row][col]

        if self.selected:
            if (row, col) in self.valid_moves:
                self._make_move(self.selected, (row, col))
            elif piece and piece.color == self.turn:
                self.selected    = (row, col)
                self.valid_moves = self._legal_moves(row, col)
            else:
                self.selected    = None
                self.valid_moves = []
        elif piece and piece.color == self.turn:
            self.selected    = (row, col)
            self.valid_moves = self._legal_moves(row, col)

        self._update_status()

    # ── Move execution ────────────────────────────────────────
    def _make_move(self, from_pos, to_pos):
        self.board.move(from_pos, to_pos)
        self.board.check_promotion()

        piece = self.board.grid[to_pos[0]][to_pos[1]]
        self.move_history.append({
            'from': from_pos, 'to': to_pos,
            'piece': piece.symbol if piece else '?'
        })

        # Switch turn
        self.turn        = 'black' if self.turn == 'white' else 'white'
        self.selected    = None
        self.valid_moves = []

        # ✅ Checkmate / Stalemate detection
        if not self._has_any_legal_move(self.turn):
            self.game_over = True
            if self.board.is_in_check(self.turn):
                # Checkmate — opponent of current turn wins
                self.winner = 'black' if self.turn == 'white' else 'white'
            else:
                # Stalemate
                self.winner = None
            self._update_status()
            return   # game_over=True will be picked up by main loop

        self._update_status()

        # Trigger AI
        if self.mode == MODE_HVA and self.turn == 'black' and not self.game_over:
            self._trigger_ai()

    # ── AI ────────────────────────────────────────────────────
    def _trigger_ai(self):
        self.ai_thinking = True
        self._update_status()

        def run():
            move = get_ai_move(self.board, depth=3)
            self._ai_move_result = move
            self.ai_thinking     = False

        threading.Thread(target=run, daemon=True).start()

    def update(self):
        """Called every frame — applies AI move when ready."""
        if (self._ai_move_result is not None
                and not self.ai_thinking
                and not self.game_over):
            move = self._ai_move_result
            self._ai_move_result = None
            self._make_move(move[0], move[1])

    def reset(self, mode=None, theme=None):
        self.__init__(self.screen, mode or self.mode, theme)

    # ── Drawing ───────────────────────────────────────────────
    def draw(self):
        self.screen.fill(BG_COLOR)
        self._draw_board()
        self._draw_highlights()
        self._draw_pieces()
        self._draw_ui()

    def _draw_board(self):
        for row in range(ROWS):
            for col in range(COLS):
                color = self.light_sq if (row+col) % 2 == 0 else self.dark_sq
                pygame.draw.rect(self.screen, color,
                    (OFFSET_X + col*SQUARE_SIZE, OFFSET_Y + row*SQUARE_SIZE,
                     SQUARE_SIZE, SQUARE_SIZE))

        # Red king highlight when in check
        if not self.game_over and self.board.is_in_check(self.turn):
            kp = self.board.find_king(self.turn)
            if kp:
                r, c = kp
                s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                s.fill((220, 50, 50, 170))
                self.screen.blit(s, (OFFSET_X + c*SQUARE_SIZE, OFFSET_Y + r*SQUARE_SIZE))

        pygame.draw.rect(self.screen, TEXT_GOLD,
                         (OFFSET_X-2, OFFSET_Y-2, BOARD_SIZE+4, BOARD_SIZE+4), 2)

        for i in range(8):
            lbl = self.small_font.render(str(8-i), True, TEXT_GRAY)
            self.screen.blit(lbl, (OFFSET_X-16, OFFSET_Y + i*SQUARE_SIZE + SQUARE_SIZE//2 - 8))
            lbl2 = self.small_font.render(chr(ord('a')+i), True, TEXT_GRAY)
            self.screen.blit(lbl2, (OFFSET_X + i*SQUARE_SIZE + SQUARE_SIZE//2 - 5,
                                    OFFSET_Y + BOARD_SIZE + 4))

    def _draw_highlights(self):
        if self.selected:
            r, c = self.selected
            s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            s.fill((*HIGHLIGHT, 180))
            self.screen.blit(s, (OFFSET_X + c*SQUARE_SIZE, OFFSET_Y + r*SQUARE_SIZE))

        for (r, c) in self.valid_moves:
            target = self.board.grid[r][c]
            s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            s.fill((*CAPTURE_SQ, 140) if target else (*MOVE_DOT, 130))
            self.screen.blit(s, (OFFSET_X + c*SQUARE_SIZE, OFFSET_Y + r*SQUARE_SIZE))

    def _draw_pieces(self):
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board.grid[row][col]
                if piece:
                    fg  = (30,30,30)    if piece.color == 'black' else (255,255,255)
                    shd = (180,180,180) if piece.color == 'black' else (80,80,80)
                    txt  = self.piece_font.render(piece.symbol, True, fg)
                    shdt = self.piece_font.render(piece.symbol, True, shd)
                    x = OFFSET_X + col*SQUARE_SIZE + (SQUARE_SIZE - txt.get_width())  // 2
                    y = OFFSET_Y + row*SQUARE_SIZE + (SQUARE_SIZE - txt.get_height()) // 2
                    self.screen.blit(shdt, (x+1, y+1))
                    self.screen.blit(txt,  (x,   y))

    def _draw_ui(self):
        st = self.ui_font.render(self.status_msg, True, TEXT_GOLD)
        self.screen.blit(st, (WIDTH//2 - st.get_width()//2, HEIGHT - 22))

        mode_txt = "👤 vs 👤" if self.mode == MODE_HVH else "👤 vs 🤖"
        ms = self.small_font.render(mode_txt, True, TEXT_GRAY)
        self.screen.blit(ms, (8, 6))

        mv = self.small_font.render(f"Moves: {len(self.move_history)}", True, TEXT_GRAY)
        self.screen.blit(mv, (WIDTH - mv.get_width() - 8, 6))

        th = self.small_font.render(f"🎨 {self.theme_name}", True, TEXT_GRAY)
        self.screen.blit(th, (WIDTH - th.get_width() - 8, 22))

        if self.ai_thinking:
            dots = "." * ((pygame.time.get_ticks() // 400) % 4)
            ts = self.ui_font.render(f"AI thinking{dots}", True, ACCENT_GREEN)
            self.screen.blit(ts, (WIDTH//2 - ts.get_width()//2, 4))