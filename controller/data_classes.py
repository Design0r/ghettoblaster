from dataclasses import dataclass


@dataclass
class Resolution:
    name: str
    x: int
    y: int

    @property
    def res(self) -> tuple[int, int]:
        return self.x, self.y


class ResolutionManager:
    _instance = None

    def __init__(self) -> None:
        pass
