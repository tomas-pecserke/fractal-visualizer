from typing import Callable
from numpy import uint8
from PIL import Image

from . import Viewport, Fractal

ColorMapper = Callable[[float], tuple[uint8, ...]]


def paint(
        fractal: Fractal,
        viewport: Viewport,
        mapper: Callable[[float], tuple[int, ...]],
        smooth: bool
):
    scale = viewport.scale
    offset = viewport.offset
    image = viewport.image
    for y in range(image.height):
        paint_row(y, scale, offset, fractal, mapper, smooth, image)


def paint_row(
        y: int,
        scale: float,
        offset: complex,
        fractal: Fractal,
        mapper: Callable[[float], tuple[int, ...]],
        smooth: bool,
        image: Image
):
    for x in range(image.width):
        c = complex(x, -y) * scale + offset
        stability = fractal.stability(c, smooth)
        color = mapper(stability)
        image.putpixel((x, y), color)
