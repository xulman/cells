import numpy

Coords = tuple[int, int, int]


class Cell:
    def __init__(self, label: int, volume: int, surface_pixels: list[Coords], centroid: Coords, is3d: bool):
        self.label: int = label
        self.volume: int = volume
        self.surface_pixels: list[Coords] = surface_pixels
        self.centroid: Coords = centroid
        self.is3d: bool = is3d
        self.roundness: float
        if is3d:
            # https://www.sciencedirect.com/science/article/pii/S1877750318304757
            self.roundness = numpy.cbrt(36 * numpy.pi * (volume ** 2)) / len(surface_pixels)
        else:
            self.roundness = (4 * numpy.pi * volume) / (len(surface_pixels) ** 2)

    def __str__(self):
        return f"Cell label: {self.label}, volume: {self.volume}, border pixels: {len(self.surface_pixels)}, centroid: {self.centroid}, roundness: {self.roundness}"
