import numpy
from tifffile import imread
from typing import Tuple

from numpy import ndarray

Coords = Tuple[int, int, int]
ImageSize = Tuple[int, int, int]


class Cell:
    def __init__(self, label, volume, surface, centroid: Coords, is3d):
        self.label = label
        self.volume = volume
        self.surface = surface
        self.centroid = centroid
        self.is3d = is3d
        if is3d:
            # https://www.sciencedirect.com/science/article/pii/S1877750318304757
            self.roundness = numpy.cbrt(36 * numpy.pi * (volume ** 2)) / surface
        else:
            self.roundness = (4 * numpy.pi * volume) / (surface ** 2)

    def __str__(self):
        return f"Cell label: {self.label}, volume: {self.volume}, border pixels: {self.surface}, centroid: {self.centroid}, roundness: {self.roundness}"


def main():
    volume = {}
    surface = {}
    cumul_coords = {}
    cells = {}

    image = imread('./data/masks_3D.tif')
    is3d = type(image[0][0]) == numpy.ndarray
    if not is3d:
        image = [image]
    size = len(image[0][0]), len(image[0]), len(image)
    for z in range(len(image)):
        print(f"processing layer {z}/{size[2] - 1}")
        for y in range(len(image[0])):
            for x in range(len(image[0][0])):
                value = image[z][y][x]
                if value != 0:
                    # volume
                    volume[value] = volume.get(value, 0) + 1
                    # surface
                    if is_pixel_at_cell_border(image, (x, y, z), value, size):
                        surface[value] = surface.get(value, 0) + 1
                    # cumulative_coords
                    coords = cumul_coords.get(value, (0, 0, 0))
                    cumul_coords[value] = coords[0] + x, coords[1] + y, coords[2] + z
    for label in volume:
        obj_volume = volume[label]
        coords = cumul_coords[label]
        centroid = round(coords[0] / obj_volume), round(coords[1] / obj_volume), round(coords[2] / obj_volume)
        cells[label] = Cell(label, obj_volume, surface[label], centroid, is3d)
        print(cells[label])


# Decides if the pixel is on the border of the object (6-connectivity)
def is_pixel_at_cell_border(image: ndarray, pixel: Coords, val: int, size: ImageSize):
    max_x, max_y, max_z = size
    max_x -= 1
    max_y -= 1
    max_z -= 1
    x, y, z = pixel

    # On the border of image:
    if x == 0 or x == max_x or y == 0 or y == max_y or (size[2] > 1 and (z == 0 or z == max_z)):
        return True

    # On the border of object:
    # offsets to the neighbors [[dx,dy,dz],[dx,dy,dz],...]; dx stands for "delta in x"
    neighs = [[0, -1, 0], [-1, 0, 0], [1, 0, 0], [0, 1, 0]]
    if size[2] > 1:
        neighs += [[0, 0, -1], [0, 0, 1]]
    for dx, dy, dz in neighs:
        if image[z + dz][y + dy][x + dx] != val:
            return True
    return False


if __name__ == "__main__":
    main()
    print("Finished")
