import pygame
from .map import Map
from .patterns import Patterns
from . import constant
import random
from .spells import Spells
from .renderer import (
    make_case, draw_entities, make_button_turn, draw_timer, draw_spells,
    compute_map_offset, map_screen_bottom,
)


def get_random_spawn_pattern(patterns_instance: Patterns) -> list[tuple]:
    try:
        r_int: int = random.randint(
            0, len(patterns_instance.spawn_patterns) - 1)
        spawn_pattern: list[tuple] = patterns_instance.spawn_patterns[r_int]
        patterns_instance.spawn_patterns.remove(spawn_pattern)
        return spawn_pattern
    except Exception:
        return []


def play_next_turn(
        map_instance: Map,
        patterns_instance: Patterns,
        spawn_pattern: list[tuple],
) -> list[tuple]:
    map_instance.place_flames(spawn_pattern)
    return get_random_spawn_pattern(patterns_instance)


def on_button_end_turn(mouse_x: int, mouse_y: int, bx: int, by: int) -> bool:
    return (bx <= mouse_x < bx + constant.BUTTON_W
            and by <= mouse_y < by + constant.BUTTON_H)


def on_spell(
        mouse_x: int,
        mouse_y: int,
        spells: list[Spells],
        spell_renders: list[tuple[pygame.Surface, int, int]],
) -> tuple[bool, None | Spells]:
    for i, (img, sx, sy) in enumerate(spell_renders):
        if (sx <= mouse_x < sx + img.get_width()
                and sy <= mouse_y < sy + img.get_height()):
            return True, spells[i]
    return False, None


if __name__ == "__main__":
    pygame.init()
    screen: pygame.Surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock: pygame.time.Clock = pygame.time.Clock()
    running: bool = True

    font_title: pygame.font.Font = pygame.font.Font(None, 50)
    font_txt: pygame.font.Font = pygame.font.Font(None, 25)

    timer_event: int = pygame.USEREVENT + 1
    timer_sec: int = constant.TIME_TURN
    timer_text: pygame.Surface = font_title.render("02:00", True, (255, 255, 255))
    pygame.time.set_timer(timer_event, 1000)

    map_instance: Map = Map()
    player = map_instance.player
    patterns_instance: Patterns = Patterns()
    spawn_pattern: list[tuple] = get_random_spawn_pattern(patterns_instance)
    previsualiation: list[tuple] = []
    spell_renders: list[tuple[pygame.Surface, int, int]] = []

    sw, sh = screen.get_width(), screen.get_height()
    avail_w = sw - constant.RIGHT_PANEL_W
    map_offset = compute_map_offset(map_instance.cases, sw, sh)
    spell_y = map_screen_bottom(map_instance.cases, map_offset) + 20
    bx = avail_w + (constant.RIGHT_PANEL_W - constant.BUTTON_W) // 2
    by = sh // 2

    while running:
        screen.fill((0, 0, 0))
        mouse_x, mouse_y = pygame.mouse.get_pos()
        next_turn: int = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == timer_event:
                if timer_sec > 0:
                    timer_sec -= 1
                    time_str = ("01:%02d" % (timer_sec - 60)
                                if timer_sec >= 60 else "00:%02d" % timer_sec)
                    timer_text = font_title.render(time_str, True, (255, 255, 255))
                else:
                    pygame.time.set_timer(timer_event, 1000)
                    timer_sec = constant.TIME_TURN
                    next_turn = 1

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if on_button_end_turn(mouse_x, mouse_y, bx, by):
                        next_turn = 1
                    is_spell, spell = on_spell(
                        mouse_x, mouse_y, player.spells, spell_renders)
                    if is_spell:
                        previsualiation = spell.previsu(
                            (player.pos_x, player.pos_y), map_instance.cases)
                        if previsualiation:
                            spell.play()
                    else:
                        previsualiation = []

        if next_turn:
            timer_sec = constant.TIME_TURN
            spawn_pattern = play_next_turn(
                map_instance, patterns_instance, spawn_pattern)

        make_case(screen, mouse_x, mouse_y, map_instance.cases,
                  previsualiation, spawn_pattern,
                  map_instance.grid_max_x, map_instance.grid_max_y,
                  map_offset, font_txt)
        draw_entities(screen, map_instance.cases, map_offset)
        make_button_turn(screen, mouse_x, mouse_y, font_title, bx, by)
        draw_timer(screen, timer_text, bx, by - 60)
        spell_renders = draw_spells(screen, mouse_x, mouse_y,
                                    player.spells, font_title, font_txt,
                                    spell_y, avail_w)

        pygame.display.update()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
