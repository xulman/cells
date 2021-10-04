import numpy
from tifffile import imread
import imagecodecs
from typing import Tuple

from numpy import ndarray

Coords = Tuple[int, int, int]
ImageSize = Tuple[int, int, int]

class Cell:
    def __init__(self, label, volume, surface, centroid: Coords):
        self.label = label
        self.volume = volume
        self.surface = surface
        self.centroid = centroid
        #https://www.sciencedirect.com/science/article/pii/S1877750318304757
        self.sphericity = numpy.cbrt(36 * numpy.pi * (volume ** 2)) / surface

    def __str__(self):
        return f"Cell label: {self.label}, volume: {self.volume}, border pixels: {self.surface}, centroid: {self.centroid}, sphericity: {self.sphericity}"


def main():
    volume = {}
    surface = {}
    cumul_coords = {}
    cells = {}

    image = imread('./data/masks_3D.tif')
    size = len(image[0][0]), len(image[0]), len(image)
    for z in range(len(image)):
        print(f"processing layer {z}")
        for y in range(len(image[0])):
            for x in range(len(image[0][0])):
                value = image[z][y][x]
                if value != 0:
                    # volume
                    volume[value] = volume.get(value, 0) + 1
                    # surface
                    if check_on_side(image, (x, y, z), value, size):
                        surface[value] = surface.get(value, 0) + 1
                    # cumulative_coords
                    coords = cumul_coords.get(value, (0, 0, 0))
                    cumul_coords[value] = coords[0] + x, coords[1] + y, coords[2] + z
    for label in volume:
        obj_volume = volume[label]
        coords = cumul_coords[label]
        centroid = round(coords[0] / obj_volume), round(coords[1] / obj_volume), round(coords[2] / obj_volume)
        cells[label] = Cell(label, obj_volume, surface[label], centroid)
        print(cells[label])


# Desides if pixel is on the side of object (6-connectivity)
def check_on_side(image: ndarray, pixel: Coords, val: int, size: ImageSize):
    max_x, max_y, max_z = size
    max_x -= 1
    max_y -= 1
    max_z -= 1
    x, y, z = pixel

    # On the border of image
    if x == 0 or x == max_x or y == 0 or y == max_y or z == 0 or z == max_z:
        return True
    # On the border of object
    if (image[z][y][x + 1] != val
            or image[z][y][x - 1] != val
            or image[z][y + 1][x] != val
            or image[z][y - 1][x] != val
            or image[z + 1][y][x] != val
            or image[z - 1][y][x] != val):
        return True
    return False


if __name__ == "__main__":
    main()
    print("Finished")
