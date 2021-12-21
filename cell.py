from typing import Tuple

import numpy

Coords = Tuple[int, int, int]


class Cell:
    def __init__(self, label, volume, surface, centroid: Coords, is3d):
        self.label: int = label
        self.volume: int = volume
        self.surface: int = surface
        self.centroid: Coords = centroid
        self.is3d: bool = is3d
        self.roundness: float
        if is3d:
            # https://www.sciencedirect.com/science/article/pii/S1877750318304757
            self.roundness = numpy.cbrt(36 * numpy.pi * (volume ** 2)) / surface
        else:
            self.roundness = (4 * numpy.pi * volume) / (surface ** 2)

    def __str__(self):
        return f"Cell label: {self.label}, volume: {self.volume}, border pixels: {self.surface}, centroid: {self.centroid}, roundness: {self.roundness}"
