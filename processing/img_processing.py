from collections import defaultdict
from tifffile import imread

from cells.distance_transform.distance_transform import create_distance_graph
from cells.project_types import Cell, CellsStore, ImageSize, Coords, Image, Label


def read_cells(image_address, bbox_border=False) -> CellsStore:
    volume: dict[Label, int] = defaultdict(int)
    surface_pixels: dict[Label, list[Coords]] = {}
    cumul_coords: dict[Label, Coords] = {}
    bbox_low: dict[Label, Coords] = {}
    bbox_high: dict[Label, Coords] = {}

    image = imread(image_address)
    image = image.tolist()
    is3d = type(image[0][0]) == list
    if not is3d:
        image = [image]

    # #TEST
    # create_distance_graph(image)
    # raise Exception("TEST")
    # #TEST

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
                    if not bbox_border:
                        if is_pixel_at_cell_border(image, (x, y, z), value, size):
                            if surface_pixels.get(value, None) is not None:
                                surface_pixels[value].append((x, y, z))
                            else:
                                surface_pixels[value] = [(x, y, z)]
                    # bounding box
                    else:
                        low = bbox_low.get(value, size)
                        high = bbox_high.get(value, (0, 0, 0))
                        x_bb_low, x_bb_high = min(x, low[0]), max(x, high[0])
                        y_bb_low, y_bb_high = min(y, low[1]), max(y, high[1])
                        z_bb_low, z_bb_high = min(z, low[2]), max(y, high[2])
                        bbox_low[value] = x_bb_low, y_bb_low, z_bb_low
                        bbox_high[value] = x_bb_high, y_bb_high, z_bb_high
                    # cumulative_coords
                    coords = cumul_coords.get(value, (0, 0, 0))
                    cumul_coords[value] = coords[0] + x, coords[1] + y, coords[2] + z

    cells: CellsStore = {}
    for label in volume:
        obj_volume = volume[label]
        coords = cumul_coords[label]
        centroid = round(coords[0] / obj_volume), round(coords[1] / obj_volume), round(coords[2] / obj_volume)
        if bbox_border:
            surface_pixels[label] = get_bbox_pixels(bbox_low[label], bbox_high[label])
        cells[label] = Cell(label, obj_volume, surface_pixels[label], centroid, is3d)
    return cells


# Decides if the pixel is on the border of the object (6-connectivity)
def is_pixel_at_cell_border(image: Image, pixel: Coords, val: int, size: ImageSize):
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


def get_bbox_pixels(bbox_low: Coords, bbox_high: Coords) -> list[Coords]:
    pixels = []
    for x in range(bbox_low[0], bbox_high[0] + 1):
        pixels.append((x, bbox_low[1], bbox_low[2]))
        pixels.append((x, bbox_high[1], bbox_low[2]))
        pixels.append((x, bbox_low[1], bbox_high[2]))
        pixels.append((x, bbox_high[1], bbox_high[2]))
    for y in range(bbox_low[1], bbox_high[1] + 1):
        pixels.append((bbox_low[0], y, bbox_low[2]))
        pixels.append((bbox_high[0], y, bbox_low[2]))
        pixels.append((bbox_low[0], y, bbox_high[2]))
        pixels.append((bbox_high[0], y, bbox_high[2]))
    for z in range(bbox_low[2], bbox_high[2] + 1):
        pixels.append((bbox_low[0], bbox_low[1], z))
        pixels.append((bbox_high[0], bbox_low[1], z))
        pixels.append((bbox_low[0], bbox_high[1], z))
        pixels.append((bbox_high[0], bbox_high[1], z))
    return pixels
