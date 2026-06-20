import pygame
from .map import Map
from .entity import TypeEntity, Player, Entity
from .patterns import Patterns
from . import constant
import random


def draw_case(
        screen: pygame.Surface,
        x: int,
        y: int,
        color: tuple,
        font: pygame.font.Font = None
) -> None:
    iso_x, iso_y = grid_to_iso(x, y)

    cx = iso_x + screen.get_width() // 2
    cy = iso_y + screen.get_height() // 4

    top = (cx, cy - constant.CASE_HEIGHT / 2)
    right = (cx + constant.CASE_WIDTH / 2, cy)
    bottom = (cx, cy + constant.CASE_HEIGHT / 2)
    left = (cx - constant.CASE_WIDTH / 2, cy)
    pygame.draw.polygon(screen, color, [top, right, bottom, left])

    if font:
        text = font.render(f"{x},{y}", True, (0, 0, 0))
        text_rect = text.get_rect(center=(cx, cy))
        print(text_rect)
        screen.blit(text, text_rect)

    pygame.draw.polygon(screen, (0, 0, 0), [top, right, bottom, left], 1)


def grid_to_iso(
        x: int,
        y: int
) -> tuple[int, int]:
    nx = (x - y) * (constant.CASE_WIDTH / 2)
    ny = (x + y) * (constant.CASE_HEIGHT / 2)

    return int(nx), int(ny)


def hover_tile(
    screen: pygame.Surface,
    screen_x: int,
    screen_y: int,
) -> tuple[int, int]:

    x = screen_x - screen.get_width() // 2
    y = screen_y - screen.get_height() // 4

    gx = (y / (constant.CASE_HEIGHT / 2) + x / (constant.CASE_WIDTH / 2)) / 2
    gy = (y / (constant.CASE_HEIGHT / 2) - x / (constant.CASE_WIDTH / 2)) / 2

    return round(gx), round(gy)


def draw_entities(
        screen: pygame.Surface,
        cases: list[dict[tuple[int, int], int | Entity]],
):
    for case in cases:
        for k, v in case.items():
            if v == 0:
                continue
            x, y = k
            iso_x, iso_y = grid_to_iso(x, y)
            cx = iso_x + screen.get_width() // 2
            cy = iso_y + screen.get_height() // 4
            match v.type_entity:
                case TypeEntity.PLAYER:
                    pygame.draw.circle(screen, [0, 0, 255], (cx, cy), 15)
                case TypeEntity.BOLGROT:
                    pygame.draw.circle(screen, [0, 255, 0], (cx, cy), 15)
                case TypeEntity.FLAME:
                    pygame.draw.circle(screen, [255, 0, 0], (cx, cy), 15)


def draw_end_turn_button(
        screen: pygame.Surface,
        font: pygame.font.Font,
        color: list[int] = None
):
    if color is None:
        color = [123, 161, 58]
    x = screen.get_width() - 600
    y = screen.get_height() - 600
    pygame.draw.rect(screen, color, [x, y, 300, 100])
    text = font.render("End turn", True, (0, 0, 0))
    screen.blit(text, (x + 75, y + 30))


def draw_timer(
        screen: pygame.Surface,
        timer_text
):
    x = screen.get_width() - 550
    y = screen.get_height() - 480
    screen.blit(timer_text, (x + 50, y))


def make_case(
        screen: pygame.Surface,
        mouse_x: int,
        mouse_y: int,
        cases: list[dict[tuple[int, int], int | Entity]],
        spawn_pattern: list[tuple],
) -> None:
    gx, gy = hover_tile(screen, mouse_x, mouse_y)

    hovered_tile = None
    if 0 <= gx < constant.GRID_MAX_X and 0 <= gy < constant.GRID_MAX_Y:
        hovered_tile = (gx, gy)

    for case in cases:
        for k, v in case.items():
            x, y = k
            if (x, y) in spawn_pattern:
                color = constant.SPAWN_COLOR_1
            elif ((y % 2 == 0 and x % 2 == 0) or
                  (y % 2 == 1 and x % 2 == 1)):
                color = constant.CASE_COLOR_1
            else:
                color = constant.CASE_COLOR_2
            if hovered_tile and hovered_tile == (x, y):
                r, g, b = color
                g += 50
                b += 50
                color = (r, g, b)
            draw_case(screen, x, y, color)


def make_button_turn(
        screen: pygame.Surface,
        mouse_x: int,
        mouse_y: int
) -> None:
    hovered_button = None
    bx, by = screen.get_width() - 600, screen.get_height() - 600
    if bx <= mouse_x < bx + 300 and by <= mouse_y < by + 100:
        hovered_button = (bx, by)
    color_button = None
    if hovered_button:
        color_button = [123 - 50, 161, 58 + 50]
    draw_end_turn_button(screen, font_txt, color_button)


def get_random_spawn_pattern(
        patterns_instance: Patterns
) -> list[tuple]:
    try:
        r_int: int = random.randint(0, len(patterns_instance.spawn_patterns) - 1)
        spawn_pattern: list[tuple] = patterns_instance.spawn_patterns[r_int]
        patterns_instance.spawn_patterns.remove(spawn_pattern)
        return spawn_pattern
    except Exception:
        return []


def play_next_turn(
        map_instance: Map,
        patterns_instance: Patterns,
        spawn_pattern: list[tuple]
) -> list[tuple]:
    map_instance.place_flames(spawn_pattern)
    return get_random_spawn_pattern(patterns_instance)


def on_button_end_turn(
        mouse_x: int,
        mouse_y: int,
):
    bx, by = screen.get_width() - 600, screen.get_height() - 600
    return bx <= mouse_x < bx + 300 and by <= mouse_y < by + 100


if __name__ == "__main__":
    pygame.init()
    screen: pygame.Surface = pygame.display.set_mode(
        (constant.SCREEN_HEIGHT, constant.SCREEN_WIDTH))
    clock: pygame.time.Clock = pygame.time.Clock()
    running: bool = True

    font: pygame.font.Font = pygame.font.Font(None, 20)
    font_txt: pygame.font.Font = pygame.font.Font(None, 50)

    timer: int = pygame.USEREVENT + 1
    timer_sec: int = constant.TIME_TURN
    timer_text: pygame.Surface = font_txt.render(
        "02:00", True, (255, 255, 255))
    pygame.time.set_timer(timer, 1000)

    map_instance: Map = Map()
    player: Player = map_instance.player
    patterns_instance: Patterns = Patterns()
    spawn_pattern: list[tuple] | None = get_random_spawn_pattern(
        patterns_instance)

    while running:
        screen.fill((0, 0, 0))
        mouse_x, mouse_y = pygame.mouse.get_pos()
        next_turn: int = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == timer:
                if timer_sec > 0:
                    timer_sec -= 1
                    if timer_sec >= 60:
                        time_str = "01:%02d" % (timer_sec - 60)
                    else:
                        time_str = "00:%02d" % timer_sec
                    timer_text = font_txt.render(
                        time_str, True, (255, 255, 255))
                else:
                    pygame.time.set_timer(timer, 1000)
                    timer_sec = constant.TIME_TURN
                    next_turn = 1

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if on_button_end_turn(mouse_x, mouse_y):
                        next_turn = 1

        if next_turn:
            timer_sec = constant.TIME_TURN
            spawn_pattern = play_next_turn(
                map_instance, patterns_instance, spawn_pattern)

        make_case(screen, mouse_x, mouse_y, map_instance.cases, spawn_pattern)
        draw_entities(screen, map_instance.cases)
        make_button_turn(screen, mouse_x, mouse_y)
        draw_timer(screen, timer_text)

        pygame.display.update()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
