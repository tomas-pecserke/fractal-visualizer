from argparse import Namespace, ArgumentParser

from .ArgTypes import image_size_type, complex_type


def cli_options(prog_name: str, args: list[str] = None) -> Namespace:
    parser = ArgumentParser(prog=prog_name)

    parser.add_argument('-d', '--dimensions', dest="size", type=image_size_type, default=[1024, 1024])
    parser.add_argument('-f', '--format', choices=['bmp', 'svg', 'stl'], default='stl')

    parser.add_argument('-vc', '--viewport-center', type=float, default=[0, 0], nargs=2)
    parser.add_argument('-vw', '--viewport-width', type=float, default=5)

    parser.add_argument('-t', '--type', choices=['mandelbrot', 'julia'], default='mandelbrot')
    parser.add_argument('-p', '--parameter', type=float, default=[0, 0], nargs=2)

    parser.add_argument('-m', '--max-iterations', type=int, default=20)
    parser.add_argument('-e', '--escape-radius', type=float, default=2)
    parser.add_argument('-s', '--smooth', action='store_true')
    parser.add_argument('-cm', '--color-map', default=None)
    parser.add_argument('-i', '--invert-color-map', action='store_true')

    return parser.parse_args(args=args)
