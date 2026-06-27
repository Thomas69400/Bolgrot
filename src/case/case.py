from __future__ import annotations
from enum import Enum
import pygame
from ..entity import Entity
from .. import constant


class CaseType(Enum):
    FREE = 0
    WALL = 1
    EMPTY = 2


class Case:
    def __init__(
        self,
        x: int,
        y: int,
        entity: Entity | None = None,
        case_type: CaseType = CaseType.FREE,
    ) -> None:
        self.x = x
        self.y = y
        self.entity: Entity | None = entity
        self.case_type: CaseType = case_type

    def contains(
        self,
        mouse_x: int,
        mouse_y: int,
        offset: tuple[int, int],
    ) -> bool:
        rx = mouse_x - offset[0]
        ry = mouse_y - offset[1]
        half_w = constant.CASE_WIDTH / 2
        half_h = constant.CASE_HEIGHT / 2
        gx = round((ry / half_h + rx / half_w) / 2)
        gy = round((ry / half_h - rx / half_w) / 2)
        return (gx, gy) == (self.x, self.y)

    def draw(
        self,
        screen: pygame.Surface,
        offset: tuple[int, int],
        color: tuple[int, int, int],
        font: pygame.font.Font | None = None,
        show_coords: bool = False,
    ) -> None:
        iso_x = int((self.x - self.y) * (constant.CASE_WIDTH / 2))
        iso_y = int((self.x + self.y) * (constant.CASE_HEIGHT / 2))
        cx = iso_x + offset[0]
        cy = iso_y + offset[1]
        top = (cx, cy - constant.CASE_HEIGHT / 2)
        right = (cx + constant.CASE_WIDTH / 2, cy)
        bottom_pt = (cx, cy + constant.CASE_HEIGHT / 2)
        left = (cx - constant.CASE_WIDTH / 2, cy)
        pygame.draw.polygon(screen, color, [top, right, bottom_pt, left])
        pygame.draw.polygon(screen, (0, 0, 0), [
                            top, right, bottom_pt, left], 1)
        if show_coords and font:
            text = font.render(f"{self.x},{self.y}", True, (0, 0, 0))
            screen.blit(text, text.get_rect(center=(cx, cy)))
