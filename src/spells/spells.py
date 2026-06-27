from __future__ import annotations
import os
import pygame
from abc import ABC, abstractmethod
from enum import Enum


class Direction(Enum):
    NORTH: tuple = (-1, 0)
    EAST: tuple = (0, 1)
    SOUTH: tuple = (1, 0)
    WEST: tuple = (0, -1)

    NORTH_WEST: tuple = (-1, -1)
    NORTH_EAST: tuple = (-1, 1)
    SOUTH_WEST: tuple = (1, -1)
    SOUTH_EAST: tuple = (1, 1)

    DIRECTIONS_LINE: list[tuple] = [
        NORTH,
        EAST,
        SOUTH,
        WEST
    ]

    DIRECTIONS_DIAGONALS: list[tuple] = [
        NORTH_WEST,
        NORTH_EAST,
        SOUTH_WEST,
        SOUTH_EAST
    ]


class TypeSpell(Enum):
    LINE: int = 2
    DIAGONAL: int = 4
    FULL: int = 8


class Spells(ABC):
    def __init__(
            self,
            name: str,
            description: str,
            cost: int,
            max_use: int,
            effects: list[str],
            type_spell: list[tuple[TypeSpell, int]],
            line_of_sight: bool = True,
            sprite=None
    ):
        super().__init__()
        self.sprite = sprite
        self.name: str = name
        self.description: str = description
        self.cost: int = cost
        self.max_use: int = max_use
        self.effects: list[str] = effects
        self.type_spell: list[tuple[TypeSpell, int]] = type_spell
        self.line_of_sight: bool = line_of_sight
        self._image: pygame.Surface | None = None

    @abstractmethod
    def play(self):
        pass

    @property
    def image(self) -> pygame.Surface:
        if self._image is None:
            self._image = pygame.image.load(
                os.path.join("./src/sprites_png", self.sprite))
        return self._image

    def contains(
        self,
        mouse_x: int,
        mouse_y: int,
        x: int,
        y: int,
    ) -> bool:
        img = self.image
        return (x <= mouse_x < x + img.get_width()
                and y <= mouse_y < y + img.get_height())

    def _draw_tooltip(
        self,
        screen: pygame.Surface,
        pos_x: int,
        pos_y: int,
        font_title: pygame.font.Font,
        font_txt: pygame.font.Font,
    ) -> None:
        from .. import constant
        height_rect = 300
        pygame.draw.rect(screen, constant.BACKGROUND_POPUP,
                         [pos_x, pos_y - height_rect, 400, height_rect])
        screen.blit(
            font_title.render(self.name, True, (255, 255, 255)),
            (pos_x, pos_y - height_rect),
        )
        screen.blit(
            font_txt.render(f"Cost: {self.cost} AP", True, (255, 255, 255)),
            (pos_x, pos_y - height_rect + 50),
        )
        for i, e in enumerate(self.effects):
            screen.blit(
                font_txt.render(str(e), True, (255, 255, 255)),
                (pos_x,
                 pos_y - height_rect + 100 + font_txt.get_height() * i),
            )
        for i, d in enumerate(self.description.split(".")):
            screen.blit(
                font_txt.render(d, True, (255, 255, 255)),
                (pos_x,
                 pos_y - height_rect + 200 + font_txt.get_height() * i),
            )

    def draw(
        self,
        screen: pygame.Surface,
        x: int,
        y: int,
        mouse_x: int,
        mouse_y: int,
        font_title: pygame.font.Font,
        font_txt: pygame.font.Font,
    ) -> None:
        if self.contains(mouse_x, mouse_y, x, y):
            self._draw_tooltip(screen, x, y, font_title, font_txt)
        screen.blit(self.image, (x, y))

    def previsu(
        self,
        pos_player: tuple[int, int],
        cases: dict
    ) -> list[tuple]:
        all_pos: list[tuple] = []
        for type_s in self.type_spell:
            t, r = type_s
            match t.value:
                case 2:
                    all_pos.extend(self.make_line(
                        pos_player,
                        cases,
                        r
                    ))
                case 4:
                    all_pos.extend(self.make_diag(
                        pos_player,
                        cases,
                        r
                    ))
                case 8:
                    print("FULL")
        return all_pos

    def make_line(
        self,
        pos_player: tuple[int, int],
        cases: dict,
        range_s: int
    ) -> list[tuple]:
        x, y = pos_player
        possible_pos: list[tuple] = []
        try:
            for direction in Direction.DIRECTIONS_LINE.value:
                dx, dy = direction
                nx, ny = x, y
                for i in range(range_s):
                    nx, ny = nx + dx, ny + dy
                    if self.is_in_map((nx, ny), cases) and \
                            not self.is_blocked_by_sight(
                                (nx, ny), cases, direction) and \
                       self.is_entity_killable((nx, ny), cases):
                        possible_pos.append((nx, ny))
            return possible_pos
        except Exception:
            return []

    def make_diag(
        self,
        pos_player: tuple[int, int],
        cases: dict,
        range_s: int
    ) -> list[tuple]:
        x, y = pos_player
        possible_pos: list[tuple] = []
        try:
            for direction in Direction.DIRECTIONS_DIAGONALS.value:
                dx, dy = direction
                nx, ny = x, y
                for i in range(range_s):
                    nx, ny = nx + dx, ny + dy
                    if self.is_in_map((nx, ny), cases) and \
                            not self.is_blocked_by_sight(
                                (nx, ny), cases, direction) and \
                       self.is_entity_killable((nx, ny), cases):
                        possible_pos.append((nx, ny))
            return possible_pos
        except Exception:
            return []

    def _find_case(self, pos: tuple, cases: list):
        for case in cases:
            if (case.x, case.y) == pos:
                return case
        return None

    def is_entity_killable(
        self,
        pos_spell: tuple,
        cases: list
    ) -> bool:
        from ..entity import Entity
        if self.line_of_sight is False:
            return True
        c = self._find_case(pos_spell, cases)
        if c is not None and isinstance(c.entity, Entity):
            return c.entity.killable
        return True

    def is_blocked_by_sight(
        self,
        pos_spell: tuple,
        cases: list,
        direction: Direction,
    ) -> bool:
        if self.line_of_sight is False:
            return False

        dx, dy = direction
        dx, dy = -1 * dx, -1 * dy
        nx, ny = pos_spell[0] + dx, pos_spell[1] + dy
        c = self._find_case((nx, ny), cases)
        return c is not None and c.entity is not None and c.entity.blocks_sight

    def is_in_map(
        self,
        pos_spell: tuple,
        cases: list
    ) -> bool:
        return self._find_case(pos_spell, cases) is not None
