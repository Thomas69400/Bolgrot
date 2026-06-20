from abc import ABC, abstractmethod


class Spells(ABC):
    def __init__(
            self,
            name: str,
            description: str,
            cost: int,
            max_use: int,
            effects: list[str],
            sprite=None
    ):
        super().__init__()
        self.sprite = sprite
        self.name: str = name
        self.description: str = description
        self.cost: int = cost
        self.max_use: int = max_use
        self.effects: list[str] = effects

    @abstractmethod
    def play(self):
        pass
