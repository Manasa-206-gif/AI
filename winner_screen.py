import pygame
import math
import random
from constants import *


class Particle:
    def __init__(self):
        self.reset(start=True)

    def reset(self, start=False):
        self.x     = random.randint(0, WIDTH)
        self.y     = random.randint(-HEIGHT, 0) if start else random.randint(-80, -10)
        self.vx    = random.uniform(-1.5, 1.5)
        self.vy    = random.uniform(2.5, 6.0)
        self.color = random.choice([
            (255,215,0),(255,80,80),(80,200,120),
            (80,140,220),(255,160,80),(200,80,220),
            (255,255,100),(100,220,255),
        ])
        self.size  = random.randint(6, 15)
        self.rot   = random.uniform(0, 360)
        self.rot_v = random.uniform(-5, 5)
        self.shape = random.choice(['rect','circle'])

    def update(self):
        self.x   += self.vx
        self.y   += self.vy
        self.rot += self.rot_v
        if self.y > HEIGHT + 20:
            self.reset()

    def draw(self, screen):
        if self.shape == 'circle':
            pygame.draw.circle(screen, self.color,
                               (int(self.x), int(self.y)), self.size//2)
        else:
            s = pygame.Surface((self.size, max(1, self.size//2)), pygame.SRCALPHA)
            s.fill((*self.color, 220))
            r = pygame.transform.rotate(s, self.rot)
            screen.blit(r, (int(self.x) - r.get_width()//2,
                            int(self.y) - r.get_height()//2))


class WinnerScreen:
    def __init__(self, screen, winner, mode, move_count, theme):
        self.screen      = screen
        self.winner      = winner       # 'white' | 'black' | None
        self.mode        = mode
        self.move_count  = move_count
        self.theme       = theme
        self.tick        = 0
        self.particles   = [Particle() for _ in range(160)] if winner else []

        self._hvh_rect = None
        self._hva_rect = None

        self.f_title  = pygame.font.SysFont("arial", 64, bold=True)
        self.f_sub    = pygame.font.SysFont("arial", 24, bold=True)
        self.f_body   = pygame.font.SysFont("arial", 17)
        self.f_small  = pygame.font.SysFont("arial", 13)
        self.f_btn    = pygame.font.SysFont("arial", 19, bold=True)
        self.f_piece  = pygame.font.SysFont("segoeuisymbol", 78)

    def update(self):
        self.tick += 1
        for p in self.particles:
            p.update()

    def draw(self):
        # ── Background ────────────────────────────────────────
        self.screen.fill((15, 13, 20))

        # Draw confetti first (behind everything)
        for p in self.particles:
            p.draw(self.screen)

        # Soft glow circle behind crown
        glow_col = (255, 215, 0) if self.winner else (120, 100, 60)
        for i in range(5):
            radius = 180 + i*45
            alpha  = max(0, 30 - i*6)
            gs = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            pygame.draw.circle(gs, (*glow_col, alpha), (WIDTH//2, 195), radius)
            self.screen.blit(gs, (0,0))

        # ── Pulsing piece symbol ──────────────────────────────
        pulse = 1.0 + 0.07 * math.sin(self.tick * 0.1)
        if self.winner == 'white':
            sym, sym_col = '♔', (255, 255, 255)
        elif self.winner == 'black':
            sym, sym_col = '♚', (190, 190, 255)
        else:
            sym, sym_col = '♛', TEXT_GOLD

        raw = self.f_piece.render(sym, True, sym_col)
        sw  = int(raw.get_width()  * pulse)
        sh  = int(raw.get_height() * pulse)
        scaled = pygame.transform.smoothscale(raw, (max(1,sw), max(1,sh)))
        self.screen.blit(scaled, (WIDTH//2 - sw//2, 42))

        # ── Winner title ──────────────────────────────────────
        if self.winner == 'white':
            title = "YOU WIN! 🎉"   if self.mode == MODE_HVA else "WHITE WINS!"
            tcol  = (255, 255, 255)
            sub   = "Congratulations! Well played." if self.mode==MODE_HVA \
                    else "White player takes the crown!"
        elif self.winner == 'black':
            title = "AI WINS! 🤖"   if self.mode == MODE_HVA else "BLACK WINS!"
            tcol  = (180, 180, 255)
            sub   = "Better luck next time!" if self.mode==MODE_HVA \
                    else "Black player takes the crown!"
        else:
            title = "STALEMATE!"
            tcol  = TEXT_GOLD
            sub   = "No winner — the game is a draw."

        # Drop shadow
        shad = self.f_title.render(title, True, (0,0,0))
        self.screen.blit(shad, (WIDTH//2 - shad.get_width()//2 + 3, 173))
        # Main text
        txt = self.f_title.render(title, True, tcol)
        self.screen.blit(txt, (WIDTH//2 - txt.get_width()//2, 170))

        # Gold underline
        uw = txt.get_width() + 30
        pygame.draw.rect(self.screen, TEXT_GOLD,
                         (WIDTH//2 - uw//2, 248, uw, 4), border_radius=2)

        # Sub line
        st = self.f_sub.render(sub, True, TEXT_GRAY)
        self.screen.blit(st, (WIDTH//2 - st.get_width()//2, 260))

        # ── Stats card ────────────────────────────────────────
        cy, cw, ch = 305, 500, 64
        cx = WIDTH//2 - cw//2
        pygame.draw.rect(self.screen, (30,30,42), (cx,cy,cw,ch), border_radius=10)
        pygame.draw.rect(self.screen, (65,65,85), (cx,cy,cw,ch), 1, border_radius=10)

        stats = [
            ("🎯 Moves",  str(self.move_count)),
            ("🎮 Mode",   "vs AI" if self.mode==MODE_HVA else "vs Human"),
            ("🎨 Theme",  self.theme),
        ]
        col_w = cw // 3
        for i,(lbl,val) in enumerate(stats):
            bx = cx + col_w*i + col_w//2
            ls = self.f_small.render(lbl, True, TEXT_GRAY)
            vs = self.f_body.render(val, True, TEXT_WHITE)
            self.screen.blit(ls, (bx - ls.get_width()//2, cy+10))
            self.screen.blit(vs, (bx - vs.get_width()//2, cy+34))
            if i < 2:
                pygame.draw.line(self.screen,(65,65,85),
                                 (cx+col_w*(i+1), cy+8),(cx+col_w*(i+1), cy+ch-8),1)

        # ── Play Again label ──────────────────────────────────
        pa = self.f_sub.render("— Play Again —", True, (100,100,115))
        self.screen.blit(pa, (WIDTH//2 - pa.get_width()//2, 388))

        mx, my = pygame.mouse.get_pos()

        # Human vs Human button
        hvh = pygame.Rect(WIDTH//2 - 215, 425, 200, 58)
        hh  = hvh.collidepoint(mx,my)
        pygame.draw.rect(self.screen, (70,100,160) if hh else (40,40,55), hvh, border_radius=10)
        pygame.draw.rect(self.screen, ACCENT_BLUE, hvh, 2, border_radius=10)
        t1  = self.f_btn.render("👤 vs 👤", True, TEXT_WHITE)
        t1b = self.f_small.render("Human vs Human", True, TEXT_GRAY)
        self.screen.blit(t1,  (hvh.centerx - t1.get_width()//2,  hvh.y+10))
        self.screen.blit(t1b, (hvh.centerx - t1b.get_width()//2, hvh.y+36))
        self._hvh_rect = hvh

        # Human vs AI button
        hva = pygame.Rect(WIDTH//2 + 15, 425, 200, 58)
        ha  = hva.collidepoint(mx,my)
        pygame.draw.rect(self.screen, (50,120,80) if ha else (40,40,55), hva, border_radius=10)
        pygame.draw.rect(self.screen, ACCENT_GREEN, hva, 2, border_radius=10)
        t2  = self.f_btn.render("👤 vs 🤖", True, TEXT_WHITE)
        t2b = self.f_small.render("Human vs AI", True, TEXT_GRAY)
        self.screen.blit(t2,  (hva.centerx - t2.get_width()//2,  hva.y+10))
        self.screen.blit(t2b, (hva.centerx - t2b.get_width()//2, hva.y+36))
        self._hva_rect = hva

        # Bottom hint
        hint = self.f_small.render("M = Main Menu", True, (60,60,75))
        self.screen.blit(hint, (WIDTH//2 - hint.get_width()//2, HEIGHT - 22))

    def handle_click(self, mx, my):
        if self._hvh_rect and self._hvh_rect.collidepoint(mx, my):
            return MODE_HVH
        if self._hva_rect and self._hva_rect.collidepoint(mx, my):
            return MODE_HVA
        return None