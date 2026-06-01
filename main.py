import pygame
import sys
from game import Game
from color_picker import ColorPicker
from winner_screen import WinnerScreen
from constants import *


def draw_menu(screen):
    screen.fill(BG_COLOR)
    title_font = pygame.font.SysFont("georgia", 52, bold=True)
    sub_font   = pygame.font.SysFont("arial", 18)
    btn_font   = pygame.font.SysFont("arial", 22, bold=True)
    small_font = pygame.font.SysFont("arial", 13)

    title = title_font.render("♟  CHESS", True, TEXT_GOLD)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 90))

    sub = sub_font.render("Select your game mode", True, TEXT_GRAY)
    screen.blit(sub, (WIDTH//2 - sub.get_width()//2, 160))
    pygame.draw.line(screen, (80,80,90), (WIDTH//2-100,190), (WIDTH//2+100,190), 1)

    buttons = []
    mx, my = pygame.mouse.get_pos()

    b1 = pygame.Rect(WIDTH//2 - 160, 220, 320, 70)
    pygame.draw.rect(screen, BUTTON_HOVER if b1.collidepoint(mx,my) else BUTTON_COLOR, b1, border_radius=10)
    pygame.draw.rect(screen, ACCENT_BLUE, b1, 2, border_radius=10)
    t1 = btn_font.render("👤  vs  👤   Human vs Human", True, TEXT_WHITE)
    screen.blit(t1, (b1.centerx - t1.get_width()//2, b1.centery - t1.get_height()//2))
    buttons.append((b1, MODE_HVH))

    b2 = pygame.Rect(WIDTH//2 - 160, 320, 320, 70)
    pygame.draw.rect(screen, BUTTON_HOVER if b2.collidepoint(mx,my) else BUTTON_COLOR, b2, border_radius=10)
    pygame.draw.rect(screen, ACCENT_GREEN, b2, 2, border_radius=10)
    t2 = btn_font.render("👤  vs  🤖   Human vs AI", True, TEXT_WHITE)
    screen.blit(t2, (b2.centerx - t2.get_width()//2, b2.centery - t2.get_height()//2))
    buttons.append((b2, MODE_HVA))

    info = [
        "Human vs Human : Two players on same screen",
        "Human vs AI    : You play White vs Minimax AI",
        "",
        "Controls:  Click to move  |  R = Restart  |  M = Menu",
    ]
    for i, line in enumerate(info):
        s = small_font.render(line, True, TEXT_GRAY)
        screen.blit(s, (WIDTH//2 - s.get_width()//2, 430 + i*22))

    deco = pygame.font.SysFont("segoeuisymbol", 28).render("♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜", True, (70,70,80))
    screen.blit(deco, (WIDTH//2 - deco.get_width()//2, HEIGHT - 50))
    return buttons


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess")
    clock = pygame.time.Clock()

    state        = MODE_MENU
    game         = None
    picker       = None
    winner_scr   = None
    menu_buttons = []
    pending_mode = None

    while True:
        # ── Events ────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if state == MODE_MENU:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for rect, mode in menu_buttons:
                        if rect.collidepoint(event.pos):
                            pending_mode = mode
                            picker = ColorPicker(screen, mode)
                            state  = MODE_COLOR

            elif state == MODE_COLOR:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    chosen_theme = picker.handle_click(*event.pos)
                    if chosen_theme:
                        game  = Game(screen, pending_mode, chosen_theme)
                        state = pending_mode
                if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                    state = MODE_MENU

            elif state in (MODE_HVH, MODE_HVA):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not game.game_over:
                        game.handle_click(*event.pos)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game.reset()
                    elif event.key == pygame.K_m:
                        state = MODE_MENU
                        game  = None

            elif state == MODE_WINNER:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    chosen = winner_scr.handle_click(*event.pos)
                    if chosen:
                        pending_mode = chosen
                        picker = ColorPicker(screen, chosen)
                        state  = MODE_COLOR
                if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                    state = MODE_MENU
                    game  = None

        # ── Update ────────────────────────────────────────────
        if state in (MODE_HVH, MODE_HVA) and game:
            # Run AI move if needed
            game.update()

            # ✅ CHECK EVERY FRAME — switch to winner screen immediately
            if game.game_over:
                winner_scr = WinnerScreen(
                    screen,
                    game.winner,
                    game.mode,
                    len(game.move_history),
                    game.theme_name
                )
                state = MODE_WINNER

        if state == MODE_WINNER and winner_scr:
            winner_scr.update()

        # ── Draw ──────────────────────────────────────────────
        if state == MODE_MENU:
            menu_buttons = draw_menu(screen)

        elif state == MODE_COLOR:
            picker.draw()

        elif state in (MODE_HVH, MODE_HVA) and game:
            game.draw()

        elif state == MODE_WINNER and winner_scr:
            winner_scr.draw()

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()