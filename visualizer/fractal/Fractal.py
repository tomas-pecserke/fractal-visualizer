from dataclasses import dataclass
from math import log
from typing import Generator, Callable

FractalSet = Callable[[complex], Generator[complex, None, None]]


def mandelbrot() -> FractalSet:
    return lambda candidate: sequence(z=0, c=candidate)


def julia(parameter: complex) -> FractalSet:
    return lambda candidate: sequence(z=candidate, c=parameter)


def sequence(c: complex, z: complex = 0) -> Generator[complex, None, None]:
    while True:
        yield z
        z = z ** 2 + c


@dataclass
class Fractal:
    fractal_set: FractalSet
    max_iterations: int
    escape_radius: float = 2.0

    def __contains__(self, c: complex) -> bool:
        return self.stability(c) == 1

    def stability(self, c: complex, smooth=False, clamp=True) -> float:
        value = self.escape_count(c, smooth) / self.max_iterations
        return max(0.0, min(value, 1.0)) if clamp else value

    def escape_count(self, candidate: complex, smooth: bool = False) -> int | float:
        iteration = 0
        for z in self.fractal_set(candidate):
            if self.max_iterations <= iteration:
                break
            if abs(z) > self.escape_radius:
                if smooth:
                    return iteration + 1 - log(log(abs(z))) / log(2)
                return iteration
            iteration += 1
        return self.max_iterations
