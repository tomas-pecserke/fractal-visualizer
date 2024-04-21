from matplotlib.colors import Colormap
from numpy import uint8

from visualizer.fractal import ColorMapper


def map_color(cm: Colormap) -> ColorMapper:
    # noinspection PyTypeChecker
    return lambda x: cm(x, bytes=True)


def black_and_white_mode(x: float) -> tuple[uint8, ...]:
    if x < 1:
        return uint8(255), uint8(255), uint8(255)
    else:
        return uint8(0), uint8(0), uint8(0)
