import pygame
from . import constant
from .game import Game
from .actions import (
    on_button_end_turn_click, on_spell_hover, on_previsu_click
)
from .renderer import (
    make_case, draw_entities, make_button_turn, draw_timer, draw_spells,
    compute_map_offset, map_screen_bottom,
)


if __name__ == "__main__":
    pygame.init()
    screen: pygame.Surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock: pygame.time.Clock = pygame.time.Clock()
    running: bool = True

    font_title: pygame.font.Font = pygame.font.Font(None, 50)
    font_txt: pygame.font.Font = pygame.font.Font(None, 25)

    timer_event: int = pygame.USEREVENT + 1
    timer_sec: int = constant.TIME_TURN
    timer_text: pygame.Surface = font_title.render(
        "02:00", True, (255, 255, 255))
    pygame.time.set_timer(timer_event, 1000)

    game: Game = Game()
    spell_renders: list[tuple[pygame.Surface, int, int]] = []

    sw, sh = screen.get_width(), screen.get_height()
    avail_w = sw - constant.RIGHT_PANEL_W
    map_offset = compute_map_offset(game.map.cases, sw, sh)
    spell_y = map_screen_bottom(game.map.cases, map_offset) + 20
    bx = avail_w + (constant.RIGHT_PANEL_W - constant.BUTTON_W) // 2
    by = sh // 2

    while running:
        screen.fill((0, 0, 0))
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == timer_event:
                if timer_sec > 0:
                    timer_sec -= 1
                    time_str = ("01:%02d" % (timer_sec - 60)
                                if timer_sec >= 60 else "00:%02d" % timer_sec)
                    timer_text = font_title.render(
                        time_str, True, (255, 255, 255))
                else:
                    pygame.time.set_timer(timer_event, 1000)
                    timer_sec = constant.TIME_TURN
                    game.end_turn()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    is_on_previsu, previsu_index = on_previsu_click(
                        mouse_x, mouse_y, game.previsualiation, map_offset)
                    clicked_spell, spell_index = on_spell_hover(
                            mouse_x, mouse_y, spell_renders)

                    if is_on_previsu:
                        game.play_selected_spell(
                            game.previsualiation[previsu_index])
                    elif on_button_end_turn_click(mouse_x, mouse_y, bx, by):
                        timer_sec = constant.TIME_TURN
                        game.end_turn()
                    elif clicked_spell:
                        game.select_spell(spell_index)
                    else:
                        game.clear_previsu()

        make_case(screen, mouse_x, mouse_y, game.map.cases,
                  game.previsualiation, game.spawn_pattern,
                  game.map.grid_max_x, game.map.grid_max_y,
                  map_offset, font_txt)
        draw_entities(screen, game.map.cases, map_offset)
        make_button_turn(screen, mouse_x, mouse_y, font_title, bx, by)
        draw_timer(screen, timer_text, bx, by - 60)
        spell_renders = draw_spells(screen, mouse_x, mouse_y,
                                    game.player.spells, font_title, font_txt,
                                    spell_y, avail_w)

        pygame.display.update()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
