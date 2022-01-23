import numpy
from numba.typed import List
from utils import distance

# reference types
ImageSize = tuple[int, int, int]
Coords = tuple[int, int, int]
PixelNativeList = list[Coords]
PixelNumbaList = List[Coords]
DistFromOneCell = dict[int, int]  # id -> distance
DistancesToCells = dict[int, int]  # distance -> id
DistMatrix = dict[int, DistancesToCells]
# CellsStore type is defined below (after the class itself)


class Cell:
    def __init__(self, label: int, volume: int, surface_pixels: PixelNativeList, centroid: Coords, is3d: bool):
        self.label: int = label
        self.volume: int = volume
        self.surface_pixels: PixelNativeList = surface_pixels
        self.surface_pixels_numba: PixelNumbaList = None  # filled on-demand
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
        return f"Cell label: {self.label}, volume: {self.volume}, border pixels: {len(self.surface_pixels)}" \
               f", centroid: {self.centroid}, roundness: {self.roundness}, avg.radius: {self.avg_radius}"

    def visualize(self, image: numpy.ndarray):
        if self.is3d:
            points_on_sphere(self.centroid, 3, self.label, image)  # centre
            points_on_sphere(self.centroid, self.avg_radius, self.label, image)  # radius
        else:
            points_on_circle(self.centroid, 3, self.label, image)
            points_on_circle(self.centroid, self.avg_radius, self.label, image)


def compute_avg_radius(centroid: Coords, surface_pixels: PixelNativeList) -> float:
    distance_sum = 0
    for pixel in surface_pixels:
        distance_sum += distance(centroid, pixel)
    return distance_sum / len(surface_pixels)


def points_on_circle(centre: Coords, radius: float, value: int, img: numpy.ndarray):
    _, Y, X = img.shape
    print(f"value {value} with centre {centre}, radius {radius}")
    # bounding box
    cx, cy, _ = centre
    min_x = max(int(cx - radius), 0)
    min_y = max(int(cy - radius), 0)
    max_x = min(int(cx + radius), X - 1)
    max_y = min(int(cy + radius), Y - 1)
    print(f"sweeping box {min_x},{min_y} -> {max_x},{max_y}")
    # for detecting circle boundary
    delta = 0.7
    radius_sq_min = (radius - delta) ** 2
    radius_sq_max = (radius + delta) ** 2
    # the drawing itself
    for y in range(min_y, max_y + 1):
        ry = (y - cy) ** 2
        for x in range(min_x, max_x + 1):
            r = (x - cx) ** 2 + ry
            if radius_sq_min < r < radius_sq_max:
                img[0][y][x] = value


def points_on_sphere(centre: Coords, radius: float, value: int, img: numpy.ndarray):
    # TBA... for now:
    points_on_circle(centre, radius, value, img)


# one more reference type
CellsStore = dict[int, Cell]
