import subprocess
import time
from argparse import Namespace
from functools import reduce
from os import unlink

import build123d
from PIL import Image
from build123d import *
from build123d import Part
from matplotlib import colormaps
from matplotlib.colors import Colormap

from visualizer.fractal import black_and_white_mode, map_color, julia, mandelbrot, paint, \
    ColorMapper, Fractal, FractalSet, Viewport
from visualizer.util import cached
from .CliOptions import cli_options

__app_name__ = 'fractal-visualizer'


def app(prog_name: str = __app_name__, args: list[str] = None):
    arguments = cli_options(prog_name=prog_name, args=args)
    print(arguments)

    fractal_set = get_fractal_set(arguments)
    color_mapper = get_color_mapper(arguments)

    image = Image.new(mode="RGB", size=arguments.size)
    fractal = Fractal(fractal_set, arguments.max_iterations, arguments.escape_radius)
    viewport_center = complex(arguments.viewport_center[0], arguments.viewport_center[1])
    viewport = Viewport(image, viewport_center, arguments.viewport_width)

    bmp_path = 'fractal.bmp'
    svg_path = 'fractal.svg'
    mesh_path = 'fractal.stl'

    print("Rendering fractal...")
    start = time.time()
    paint(fractal, viewport, color_mapper, smooth=arguments.smooth)
    image.save(bmp_path)
    end = time.time()
    print('Rendering completed in', end - start, 'seconds')

    if arguments.format == 'bmp':
        return

    print("Tracing bitmap to vector...")
    start = time.time()
    svg_trace(bmp_path, svg_path)
    unlink(bmp_path)
    end = time.time()
    print("Tracing completed in", end - start, 'seconds')

    if arguments.format == 'svg':
        return

    print("Converting to mesh...")
    start = time.time()
    mesh = build_mesh(svg_path, arguments)
    build123d.export_stl(mesh, mesh_path)
    unlink(svg_path)
    end = time.time()
    print("Mesh completed in", end - start, 'seconds')


def get_fractal_set(arguments: Namespace) -> FractalSet:
    match arguments.type:
        case 'julia':
            parameter = complex(arguments.parameter[0], arguments.parameter[1])
            return julia(parameter)
        case _:
            return mandelbrot()


def get_color_mapper(arguments: Namespace) -> ColorMapper:
    color_mapper: ColorMapper
    if arguments.color_map is None:
        if arguments.invert_color_map:
            return lambda x: black_and_white_mode(1-x)
        return black_and_white_mode
    else:
        colormap: Colormap = colormaps[arguments.color_map]
        if arguments.invert_color_map:
            colormap = colormap.reversed()
        return cached(map_color(colormap))


def svg_trace(input_path: str, output_path: str) -> None:
    subprocess.run(
        [
            'potrace',
            '--output', output_path,
            '--backend', 'svg',
            '--turdsize', str(100),
            '--alphamax', str(1),
            # '--longcurve',
            '--opttolerance', str(0.2),
            '--unit', str(10),
            input_path
        ],
        shell=True,
        check=True
    )


def build_mesh(input_path: str, arguments: Namespace) -> Part:
    imported = import_svg(input_path)
    size = reduce(
        lambda a, b: a.add(b),
        map(lambda s: s.bounding_box(), imported)
    ).size
    max_dimension = max(size.X, size.Y)
    factor = 225 / max_dimension
    # noinspection PyTypeChecker
    imported: ShapeList[Wire | Face] = list(map(lambda s: s.scale(factor), imported))
    imported.sort(key=lambda s: s.bounding_box().size.length, reverse=True)

    layer_height = 1

    with BuildPart() as mesh:
        layer = 1
        for shape in imported:
            with BuildSketch() as sketch:
                add(shape)
            extrude(amount=layer * layer_height)
            layer += 1

    return mesh.part
