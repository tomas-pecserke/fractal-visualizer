import subprocess
import time
from argparse import Namespace
from os import unlink

import build123d
from PIL import Image
from build123d import *
from matplotlib import colormaps

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
    export_meshes(svg_path, mesh_path)
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
        return black_and_white_mode
    else:
        colormap = colormaps[arguments.color_map]
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


def export_meshes(input_path: str, output_path: str) -> None:
    with BuildPart() as svg_part:
        with BuildSketch() as svg_sketch:
            imported = import_svg(input_path)
            add(imported)
            size = svg_sketch.sketch.bounding_box().size
            max_dimension = max(size.X, size.Y, size.Z)
            factor = 225 / max_dimension
            scale(by=(factor, factor, 1))
        extrude(amount=2)
    build123d.export_stl(svg_part.part, output_path, tolerance=0.01)
