from __future__ import annotations
import pygame
from .. import constant


class Button:
    def __init__(
        self,
        screen: pygame.Surface,
        font: pygame.font.Font,
        x: int,
        y: int,
        label: str,
    ):
        self.screen = screen
        self.font = font
        self.x = x
        self.y = y
        self.label = label

    def contains(self, mouse_x: int, mouse_y: int) -> bool:
        return (self.x <= mouse_x < self.x + constant.BUTTON_W
                and self.y <= mouse_y < self.y + constant.BUTTON_H)

    def draw(self, mouse_x: int, mouse_y: int) -> None:
        color = [73, 161, 108] if self.contains(
            mouse_x, mouse_y) else [123, 161, 58]
        pygame.draw.rect(
            self.screen, color,
            [self.x, self.y, constant.BUTTON_W, constant.BUTTON_H],
        )
        text = self.font.render(self.label, True, (0, 0, 0))
        self.screen.blit(text, (
            self.x + (constant.BUTTON_W - text.get_width()) // 2,
            self.y + (constant.BUTTON_H - text.get_height()) // 2,
        ))
