import random
import math


class RainDrop:
    """A single falling raindrop. Speed and wind can be tuned per weather type."""

    def __init__(self, max_x: int, max_y: int):
        self.max_x = max_x
        self.max_y = max_y
        self._randomize(initial=True)

    def _randomize(self, initial=False):
        self.x     = random.uniform(0, self.max_x)
        self.y     = random.uniform(-self.max_y * 0.5, 0) if initial else 0
        self.speed = random.uniform(1.2, 2.0)
        self.char  = random.choice(["|", "|", "╎"])

    def update(self, wind: float = 0.15):
        self.y += self.speed
        self.x += wind
        if self.y > self.max_y or self.x > self.max_x:
            self._randomize()


class Snowflake:
    """A drifting snowflake that sways side-to-side via a sine wave."""

    CHARS = ["*", "*", "·", "•", "+", "·"]

    def __init__(self, max_x: int, max_y: int):
        self.max_x = max_x
        self.max_y = max_y
        self._randomize(initial=True)

    def _randomize(self, initial=False):
        self.x          = random.uniform(0, self.max_x)
        self.y          = random.uniform(-self.max_y * 0.3, 0) if initial else -2
        self.speed      = random.uniform(0.3, 0.9)
        self.drift_freq = random.uniform(0.05, 0.15)
        self.t          = random.uniform(0, math.pi * 2)
        self.char       = random.choice(self.CHARS)

    def update(self):
        self.y  += self.speed
        self.t  += self.drift_freq
        self.x  += math.sin(self.t) * 0.4
        if self.y > self.max_y:
            self._randomize()


class Cloud:
    """A multi-line ASCII cloud drifting slowly to the right."""

    def __init__(self, max_x: int, row: int, shape: list[str]):
        self.max_x = max_x
        self.y     = row
        self.shape = shape
        self.width = max(len(line) for line in shape)
        self.x     = float(random.randint(-5, max_x))
        self.speed = random.uniform(0.05, 0.15)

    def update(self):
        self.x += self.speed
        if self.x > self.max_x + self.width:
            self.x = float(-self.width - 5)