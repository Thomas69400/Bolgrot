from __future__ import annotations
import os
import pygame
from .case import Case
from . import constant
from .entity import TypeEntity
from .spells import Spells


def grid_to_iso(x: int, y: int) -> tuple[int, int]:
    nx = (x - y) * (constant.CASE_WIDTH / 2)
    ny = (x + y) * (constant.CASE_HEIGHT / 2)
    return int(nx), int(ny)


def compute_map_offset(
        cases: list[Case],
        screen_w: int,
        screen_h: int,
        spell_bar_h: int = 120,
) -> tuple[int, int]:
    """Screen pixel position of iso origin (0,0) that centers the map."""
    iso_xs = [case.y * constant.CASE_WIDTH for case in cases]
    iso_ys = [(case.x - case.y) * constant.CASE_HEIGHT // 2 for case in cases]
    iso_cx = (min(iso_xs) + max(iso_xs)) // 2
    iso_cy = (min(iso_ys) + max(iso_ys)) // 2
    avail_w = screen_w - constant.RIGHT_PANEL_W
    avail_h = screen_h - spell_bar_h
    return avail_w // 2 - iso_cx, avail_h // 2 - iso_cy


def map_screen_bottom(cases: list[Case], offset: tuple[int, int]) -> int:
    """Y screen coordinate of the lowest tile's bottom edge."""
    iso_ys = [(case.x - case.y) * constant.CASE_HEIGHT // 2 for case in cases]
    return offset[1] + max(iso_ys) + constant.CASE_HEIGHT // 2


def hover_tile(
        mouse_x: int,
        mouse_y: int,
        offset: tuple[int, int],
) -> tuple[int, int]:
    x = mouse_x - offset[0]
    y = mouse_y - offset[1]
    gy = x / constant.CASE_WIDTH
    gx = 2 * y / constant.CASE_HEIGHT + gy
    return round(gx), round(gy)


def draw_case(
        screen: pygame.Surface,
        x: int,
        y: int,
        color: tuple,
        offset: tuple[int, int],
        font: pygame.font.Font = None,
) -> None:
    iso_x, iso_y = grid_to_iso(x, y)
    cx = iso_x + offset[0]
    cy = iso_y + offset[1]
    top = (cx, cy - constant.CASE_HEIGHT / 2)
    right = (cx + constant.CASE_WIDTH / 2, cy)
    bottom_pt = (cx, cy + constant.CASE_HEIGHT / 2)
    left = (cx - constant.CASE_WIDTH / 2, cy)
    pygame.draw.polygon(screen, color, [top, right, bottom_pt, left])
    pygame.draw.polygon(screen, (0, 0, 0), [top, right, bottom_pt, left], 1)

    if font:
        text = font.render(f"{x},{y}", True, (0, 0, 0))
        screen.blit(text, text.get_rect(center=(cx, cy)))


def draw_entities(
        screen: pygame.Surface,
        cases: list[Case],
        offset: tuple[int, int],
) -> None:
    for case in cases:
        x, y = case.x, case.y
        v = case.entity
        if v is None:
            continue
        iso_x, iso_y = grid_to_iso(x, y)
        cx = iso_x + offset[0]
        cy = iso_y + offset[1]
        match v.type_entity:
            case TypeEntity.PLAYER:
                pygame.draw.circle(screen, [0, 0, 255], (cx, cy), 15)
            case TypeEntity.BOLGROT:
                pygame.draw.circle(screen, [0, 255, 0], (cx, cy), 15)
            case TypeEntity.FLAME:
                pygame.draw.circle(screen, [255, 0, 0], (cx, cy), 15)


def make_case(
        screen: pygame.Surface,
        mouse_x: int,
        mouse_y: int,
        cases: list[Case],
        previsualiation: list[tuple],
        spawn_pattern: list[tuple],
        grid_max_x: int,
        grid_max_y: int,
        offset: tuple[int, int],
        font_txt: pygame.font.Font = None,
) -> None:
    gx, gy = hover_tile(mouse_x, mouse_y, offset)
    hovered = (gx, gy) if 0 <= gx <= grid_max_x and \
        0 <= gy <= grid_max_y else None

    for case in cases:
        x, y = case.x, case.y
        if (x, y) in previsualiation:
            color = constant.PREVISU_COLO
        elif (x, y) in spawn_pattern:
            color = constant.SPAWN_COLOR_1
        elif (y % 2 == 0 and x % 2 == 0) or (y % 2 == 1 and x % 2 == 1):
            color = constant.CASE_COLOR_1
        else:
            color = constant.CASE_COLOR_2
        if hovered == (x, y):
            r, g, b = color
            color = (r, g + 50, b + 50)
        draw_case(screen, x, y, color, offset, font_txt)


def draw_end_turn_button(
        screen: pygame.Surface,
        font: pygame.font.Font,
        bx: int,
        by: int,
        color: list[int] = None,
) -> None:
    if color is None:
        color = [123, 161, 58]
    pygame.draw.rect(
        screen, color, [bx, by, constant.BUTTON_W, constant.BUTTON_H])
    text = font.render("End turn", True, (0, 0, 0))
    screen.blit(text, (
        bx + (constant.BUTTON_W - text.get_width()) // 2,
        by + (constant.BUTTON_H - text.get_height()) // 2,
    ))


def draw_timer(
        screen: pygame.Surface,
        timer_text: pygame.Surface,
        bx: int,
        by: int,
) -> None:
    screen.blit(
        timer_text, (bx + (constant.BUTTON_W -
                           timer_text.get_width()) // 2, by))


def make_button_turn(
        screen: pygame.Surface,
        mouse_x: int,
        mouse_y: int,
        font_title: pygame.font.Font,
        bx: int,
        by: int,
) -> None:
    hovering = bx <= mouse_x < bx + \
        constant.BUTTON_W and by <= mouse_y < by + constant.BUTTON_H
    draw_end_turn_button(screen, font_title, bx, by, [
                         73, 161, 108] if hovering else None)


def show_spell_data(
        screen: pygame.Surface,
        spell: Spells,
        pos_x: int,
        pos_y: int,
        font_title: pygame.font.Font,
        font_txt: pygame.font.Font,
) -> None:
    height_rect = 300
    pygame.draw.rect(screen, constant.BACKGROUND_POPUP,
                     [pos_x, pos_y - height_rect, 400, height_rect])
    screen.blit(font_title.render(spell.name, True, (255, 255, 255)),
                (pos_x, pos_y - height_rect))
    screen.blit(font_txt.render(f"Cost: {spell.cost} AP",
                                True, (255, 255, 255)),
                (pos_x, pos_y - height_rect + 50))
    for i, e in enumerate(spell.effects):
        screen.blit(font_txt.render(str(e), True, (255, 255, 255)),
                    (pos_x, pos_y - height_rect + 100 +
                     font_txt.get_height() * i))
    for i, d in enumerate(spell.description.split(".")):
        screen.blit(font_txt.render(d, True, (255, 255, 255)),
                    (pos_x, pos_y - height_rect + 200 +
                     font_txt.get_height() * i))


def draw_spells(
        screen: pygame.Surface,
        mouse_x: int,
        mouse_y: int,
        spells: list[Spells],
        font_title: pygame.font.Font,
        font_txt: pygame.font.Font,
        spell_y: int,
        avail_w: int,
) -> list[tuple[pygame.Surface, int, int]]:
    """Draw spell icons centered in avail_w. Returns (image, x, y)
    for each spell."""
    images = [
        pygame.image.load(os.path.join("./src/sprites_png", s.sprite))
        for s in spells
    ]
    total_w = sum(img.get_width() for img in images) + \
        constant.SPELL_GAP * max(0, len(images) - 1)
    x = (avail_w - total_w) // 2
    renders: list[tuple[pygame.Surface, int, int]] = []

    for s, img in zip(spells, images):
        renders.append((img, x, spell_y))
        if x <= mouse_x < x + img.get_width() and \
                spell_y <= mouse_y < spell_y + img.get_height():
            show_spell_data(screen, s, x, spell_y, font_title, font_txt)
        screen.blit(img, (x, spell_y))
        x += img.get_width() + constant.SPELL_GAP

    return renders
