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
        # FIXME: this is most likely only for 3D...
        # FIXME: either calculate outside, or pass 2D/3D flag inside here
        self.sphericity = numpy.cbrt(36 * numpy.pi * (volume ** 2)) / surface

    def __str__(self):
        return f"Cell label: {self.label}, volume: {self.volume}, border pixels: {self.surface}, centroid: {self.centroid}, sphericity: {self.sphericity}"


def main():
    volume = {}
    surface = {}
    cumul_coords = {}
    cells = {}

    image = imread('./data/masks_3D.tif')
    # FIXME: wrap 'image' with a 3D version with 3rd dim of len() = 1
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
                    if is_pixel_at_cell_border(image, (x, y, z), value, size):
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


# Decides if the pixel is on the border of the object (6-connectivity)
def is_pixel_at_cell_border(image: ndarray, pixel: Coords, val: int, size: ImageSize):
    max_x, max_y, max_z = size
    max_x -= 1
    max_y -= 1
    max_z -= 1
    x, y, z = pixel

    # On the border of image:
    # FIXME: will be always true for 2D images...
    # FIXME: create two main branches here, one for 2D an for 3D
    if x == 0 or x == max_x or y == 0 or y == max_y or z == 0 or z == max_z:
        return True

    # On the border of object:
    # offsets to the neighbors [[dx,dy,dz],[dx,dy,dz],...]; dx stands for "delta in x"
    neigs = [[0,0,-1], [0,-1,0], [-1,0,0], [1,0,0], [0,1,0], [0,0,1]]
    for dx,dy,dz in neigs:
        if image[z+dz][y+dy][x+dx] != val:
            return True
    return False


if __name__ == "__main__":
    main()
    print("Finished")
