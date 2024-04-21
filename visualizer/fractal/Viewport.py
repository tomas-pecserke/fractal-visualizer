from dataclasses import dataclass

from PIL.Image import Image


@dataclass
class Viewport:
    image: Image
    center: complex
    width: float

    @property
    def height(self):
        return self.scale * self.image.height

    @property
    def offset(self) -> complex:
        return self.center + complex(-self.width, self.height) / 2

    @property
    def scale(self) -> float:
        return self.width / self.image.width

    def __iter__(self):
        for y in range(self.image.height):
            for x in range(self.image.width):
                yield complex(x, -y) * self.scale + self.offset
