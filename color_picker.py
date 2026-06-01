import pygame
from constants import *


class ColorPicker:
    """Board colour/theme selection screen shown before each game."""

    def __init__(self, screen, mode):
        self.screen = screen
        self.mode   = mode          # which game mode was chosen
        self.selected_idx = 0       # default = Classic

        self.title_font = pygame.font.SysFont("georgia", 38, bold=True)
        self.sub_font   = pygame.font.SysFont("arial",   16)
        self.btn_font   = pygame.font.SysFont("arial",   18, bold=True)
        self.lbl_font   = pygame.font.SysFont("arial",   13)

        self._theme_rects = []
        self._start_rect  = None

    def draw(self):
        self.screen.fill(BG_COLOR)

        # Title
        title = self.title_font.render("🎨  Choose Board Colour", True, TEXT_GOLD)
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 28))

        sub_txt = "Human vs Human" if self.mode == MODE_HVH else "Human vs AI"
        sub = self.sub_font.render(f"Mode: {sub_txt}  —  pick a theme then press Start", True, TEXT_GRAY)
        self.screen.blit(sub, (WIDTH//2 - sub.get_width()//2, 76))

        # Theme grid: 4 columns × 2 rows
        cols = 4
        cell_w, cell_h = 148, 148
        pad_x = (WIDTH - cols * cell_w) // 2
        pad_y = 110

        self._theme_rects = []
        mx, my = pygame.mouse.get_pos()

        for idx, (name, light, dark) in enumerate(BOARD_THEMES):
            row = idx // cols
            col = idx % cols
            x = pad_x + col * cell_w
            y = pad_y + row * cell_h
            rect = pygame.Rect(x + 6, y + 6, cell_w - 12, cell_h - 12)
            self._theme_rects.append(rect)

            hover = rect.collidepoint(mx, my)
            selected = (idx == self.selected_idx)

            # Draw mini chessboard preview
            sq = (cell_h - 40) // 4
            board_x = rect.x + (rect.w - sq * 4) // 2
            board_y = rect.y + 6
            for r in range(4):
                for c in range(4):
                    color = light if (r + c) % 2 == 0 else dark
                    pygame.draw.rect(self.screen, color,
                                     (board_x + c * sq, board_y + r * sq, sq, sq))
            # Board border
            border_col = TEXT_GOLD if selected else ((120,120,130) if hover else (60,60,70))
            border_w   = 3 if selected else (2 if hover else 1)
            pygame.draw.rect(self.screen, border_col,
                             (board_x - 1, board_y - 1, sq * 4 + 2, sq * 4 + 2), border_w)

            # Card background
            card_col = (55, 55, 65) if (selected or hover) else (40, 40, 48)
            pygame.draw.rect(self.screen, card_col, rect, border_radius=8)
            # Redraw preview on top of card bg — draw board again after card
            for r in range(4):
                for c in range(4):
                    color = light if (r + c) % 2 == 0 else dark
                    pygame.draw.rect(self.screen, color,
                                     (board_x + c * sq, board_y + r * sq, sq, sq))
            pygame.draw.rect(self.screen, border_col,
                             (board_x - 1, board_y - 1, sq * 4 + 2, sq * 4 + 2), border_w)

            # Theme name
            lbl = self.lbl_font.render(name, True, TEXT_GOLD if selected else TEXT_GRAY)
            self.screen.blit(lbl, (rect.centerx - lbl.get_width()//2,
                                   board_y + sq * 4 + 6))

            # Colour swatches
            swatch_y = board_y + sq * 4 + 22
            for ci, col_val in enumerate([light, dark]):
                pygame.draw.rect(self.screen, col_val,
                                 (rect.x + 14 + ci * 22, swatch_y, 18, 12),
                                 border_radius=3)

            # Selected tick
            if selected:
                tick = self.btn_font.render("✓", True, TEXT_GOLD)
                self.screen.blit(tick, (rect.right - tick.get_width() - 6, rect.y + 4))

        # ── Start button ──────────────────────────────────────
        btn_w, btn_h = 220, 52
        btn_x = WIDTH // 2 - btn_w // 2
        btn_y = HEIGHT - 76
        self._start_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)
        btn_hover = self._start_rect.collidepoint(mx, my)
        pygame.draw.rect(self.screen, BUTTON_HOVER if btn_hover else BUTTON_COLOR,
                         self._start_rect, border_radius=10)
        pygame.draw.rect(self.screen, TEXT_GOLD, self._start_rect, 2, border_radius=10)
        start_txt = self.btn_font.render("▶  Start Game", True, TEXT_GOLD)
        self.screen.blit(start_txt, (self._start_rect.centerx - start_txt.get_width()//2,
                                     self._start_rect.centery - start_txt.get_height()//2))

        # Hint
        hint = self.lbl_font.render("M = back to menu", True, (70, 70, 80))
        self.screen.blit(hint, (WIDTH//2 - hint.get_width()//2, HEIGHT - 18))

    def handle_click(self, mx, my):
        """Returns chosen theme tuple if Start pressed, or None."""
        for idx, rect in enumerate(self._theme_rects):
            if rect.collidepoint(mx, my):
                self.selected_idx = idx
                return None
        if self._start_rect and self._start_rect.collidepoint(mx, my):
            return BOARD_THEMES[self.selected_idx]
        return None