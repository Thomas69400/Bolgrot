from __future__ import annotations
import os
import pygame
from abc import ABC, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING

from ..BFS import BFS


if TYPE_CHECKING:
    from ..entity import Player
    from ..map import Map
    from ..case import Case


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
            bfs: BFS,
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
        self.BFS: BFS = bfs

    @abstractmethod
    def play(
        self,
        map: Map,
        player: Player,
        tile_clicked: tuple[int, int],
    ) -> None:
        pass

    @abstractmethod
    def next_turn(
        self,
    ) -> None:
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

    def _find_case(
        self,
        pos: tuple,
        cases: list
    ) -> Case | None:
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

    def attract_flames(
        self,
        cases: list[Case],
        tile_clicked: tuple[int, int] = None,
        player: Player = None,
        killable: bool = True
    ) -> None:
        """Attract Flames towards the player position for 1 case."""
        from ..entity import Flame, Bolgrot, Player
        from ..case import CaseType
        if tile_clicked is not None:
            pos_x, pos_y = tile_clicked
        elif player is not None:
            pos_x, pos_y = player.pos_x, player.pos_y
        else:
            raise ValueError(
                "Either tile_clicked or player must be provided.")

        flame_cases = [
            case for case in cases
            if isinstance(case.entity, Flame)
            and (case.x, case.y) != (pos_x, pos_y)
        ]
        flame_cases.sort(
            key=lambda c: abs(c.x - pos_x) + abs(c.y - pos_y)
        )
        for case in flame_cases:
            dx = pos_x - case.x
            dy = pos_y - case.y
            sx = (dx > 0) - (dx < 0)
            sy = (dy > 0) - (dy < 0)
            if abs(dx) > abs(dy):
                step = (case.x + sx, case.y)
            elif abs(dy) > abs(dx):
                step = (case.x, case.y + sy)
            else:
                step = (case.x + sx, case.y + sy)
            new_case = self._find_case(step, cases)
            if new_case is None or new_case.case_type == CaseType.WALL:
                path = self.BFS.find_path(
                    (case.x, case.y),
                    (pos_x, pos_y)
                )
                new_case = self._find_case(path, cases) \
                    if path is not None else None
            if new_case is None or new_case.case_type == CaseType.WALL:
                continue
            if isinstance(new_case.entity, Bolgrot):
                continue
            elif isinstance(new_case.entity, (Flame, Player)) and killable:
                player.hp = 0
            elif new_case.entity is None:
                new_case.entity = case.entity
                case.entity = None

    def push_flames(
        self,
        player: Player,
        cases: list[Case],
    ) -> None:
        """Push Flames away from the player position for 1 case if
        they are next to the player. (diagonals included)"""
        from ..entity import Flame, Bolgrot, Player
        from ..case import CaseType
        flame_cases = [
            case for case in cases
            if isinstance(case.entity, Flame)
            and (case.x, case.y) != (player.pos_x, player.pos_y)
            and abs(case.x - player.pos_x) <= 1
            and abs(case.y - player.pos_y) <= 1
        ]
        for case in flame_cases:
            dx = case.x - player.pos_x
            dy = case.y - player.pos_y
            sx = (dx > 0) - (dx < 0)
            sy = (dy > 0) - (dy < 0)
            if abs(dx) > abs(dy):
                step = (case.x + sx, case.y)
            elif abs(dy) > abs(dx):
                step = (case.x, case.y + sy)
            else:
                step = (case.x + sx, case.y + sy)
            new_case = self._find_case(step, cases)
            if new_case is None or new_case.case_type == CaseType.WALL:
                path = self.BFS.find_path(
                    (case.x, case.y),
                    (player.pos_x, player.pos_y)
                )
                new_case = self._find_case(path, cases)
            if new_case is None or new_case.case_type == CaseType.WALL:
                continue
            if isinstance(new_case.entity, Bolgrot):
                continue
            elif isinstance(new_case.entity, (Flame, Player)):
                player.hp = 0
            elif new_case.entity is None:
                new_case.entity = case.entity
                case.entity = None
