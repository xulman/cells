from collections import defaultdict
from tifffile import imread
from cells.processing.cell import Cell, CellsStore, ImageSize, Coords


def read_cells(image_address) -> CellsStore:
    volume: dict[int, int] = defaultdict(int)
    surface_pixels: dict[int, list[Coords]] = defaultdict(list)
    cumul_coords: dict[int, Coords] = {}

    image = imread(image_address)
    image = image.tolist()
    is3d = type(image[0][0]) == list
    if not is3d:
        image = [image]

    size = len(image[0][0]), len(image[0]), len(image)
    print(f"Image size: {size}")
    for z in range(size[2]):
        for y in range(size[1]):
            for x in range(size[0]):
                value = image[z][y][x]
                if value != 0:
                    # volume
                    volume[value] += 1
                    # surface
                    if is_pixel_at_cell_border(image, (x, y, z), value, size):
                        surface_pixels[value].append((x, y, z))
                    # cumulative_coords
                    coords = cumul_coords.get(value, (0, 0, 0))
                    cumul_coords[value] = coords[0] + x, coords[1] + y, coords[2] + z

    cells: CellsStore = {}
    for label in volume:
        obj_volume = volume[label]
        coords = cumul_coords[label]
        centroid = round(coords[0] / obj_volume), round(coords[1] / obj_volume), round(coords[2] / obj_volume)
        cells[label] = Cell(label, obj_volume, surface_pixels[label], centroid, is3d)
    return cells


# Decides if the pixel is on the border of the object (6-connectivity)
def is_pixel_at_cell_border(image: list[list[list[int]]], pixel: Coords, val: int, size: ImageSize):
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
