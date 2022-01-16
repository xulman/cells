import numpy
from numba.typed import List

# reference types
ImageSize = tuple[int, int, int]
Coords = tuple[int, int, int]
PixelNativeList = list[Coords]
PixelNumbaList = List[Coords]
DistFromOneCell = dict[int, int]  # id -> distance
DistancesToCells = dict[int, int] # distance -> id
DistMatrix = dict[int, DistancesToCells]
#CellsStore type is defined below (after the class itself)

from utils import distance


class Cell:
    def __init__(self, label: int, volume: int, surface_pixels: PixelNativeList, centroid: Coords, is3d: bool):
        self.label: int = label
        self.volume: int = volume
        self.surface_pixels: PixelNativeList = surface_pixels
        self.surface_pixels_numba: PixelNumbaList = None # filled on-demand
        self.centroid: Coords = centroid
        self.is3d: bool = is3d
        self.roundness: float
        if is3d:
            # https://www.sciencedirect.com/science/article/pii/S1877750318304757
            self.roundness = numpy.cbrt(36 * numpy.pi * (volume ** 2)) / len(surface_pixels)
        else:
            self.roundness = (4 * numpy.pi * volume) / (len(surface_pixels) ** 2)
        self.avg_radius: float = compute_avg_radius(centroid, surface_pixels)


    def __str__(self):
        return f"Cell label: {self.label}, volume: {self.volume}, border pixels: {len(self.surface_pixels)}, centroid: {self.centroid}, roundness: {self.roundness}"


def compute_avg_radius(centroid: Coords, surface_pixels: PixelNativeList) -> float:
    distance_sum = 0
    for pixel in surface_pixels:
        distance_sum += distance(centroid, pixel)
    return distance_sum / len(surface_pixels)


# one more reference type
CellsStore = dict[int, Cell]