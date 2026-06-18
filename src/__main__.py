import pygame
from .map import Map
from . import constant


def draw_case(
        x: int,
        y: int,
        color: tuple,
        screen,
        offset_x: int,
        offset_y: int
) -> None:
    rect: pygame.Rect = pygame.Rect(
        constant.CASE_SIZE * x + offset_x,
        constant.CASE_SIZE * y + offset_y,
        constant.CASE_SIZE,
        constant.CASE_SIZE
    )
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, (0, 0, 0), rect, 1)


def get_tile_at_mouse(
        mouse_x: int,
        mouse_y: int,
        screen,
        offset_x: int,
        offset_y: int
) -> tuple[int, int] | None:

    x = (mouse_x - offset_x) // constant.CASE_SIZE
    y = (mouse_y - offset_y) // constant.CASE_SIZE

    if 0 <= x < constant.GRID_MAX_X and 0 <= y < constant.GRID_MAX_Y:
        return x, y
    return None


def get_offsets(
        screen
) -> tuple[int, int]:
    grid_width = constant.GRID_MAX_X * constant.CASE_SIZE
    grid_height = constant.GRID_MAX_Y * constant.CASE_SIZE
    offset_x: int = (screen.get_width() - grid_width) // 2
    offset_y: int = (screen.get_height() - grid_height) // 2

    return offset_x, offset_y


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((constant.SCREEN_HEIGHT,
                                      constant.SCREEN_WIDTH))
    clock = pygame.time.Clock()
    running = True

    map_instance: Map = Map()

    off_x, off_y = get_offsets(screen)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        mouse_x, mouse_y = pygame.mouse.get_pos()
        hovered_tile = get_tile_at_mouse(mouse_x, mouse_y,
                                         screen, off_x, off_y)

        for x, case in enumerate(map_instance.cases):
            for y, _ in enumerate(case):
                color: tuple[int, int, int] = constant.CASE_COLOR_1 \
                    if x % 2 == 0 else constant.CASE_COLOR_2
                if hovered_tile and hovered_tile == (x, y):
                    r, g, b = color
                    g += 50
                    b += 50
                    color = (r, g, b)
                draw_case(x, y, color, screen, off_x, off_y)

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
