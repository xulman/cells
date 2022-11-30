import numpy as np
from tifffile import imwrite

from cells.project_types import Graph, Image
from scipy import ndimage
from skimage.morphology import skeletonize, thin


def create_distance_graph(image: Image) -> Graph:
    size = len(image[0][0]), len(image[0]), len(image)
    for z in range(size[2]):
        for y in range(size[1]):
            for x in range(size[0]):
                value = image[z][y][x]
                if value != 0 or y in (0, size[1]-1) or x in (0, size[0]-1):
                    image[z][y][x] = 0
                else:
                    image[z][y][x] = 1

    img = ndimage.distance_transform_edt(image, return_distances=True)
    img /= np.max(np.abs(img))
    # for z in range(size[2]):
    #     for y in range(1, size[1]-1):
    #         for x in range(1, size[0]-1):
    #             value = img[z][y][x]
    #             if x == 748 and y == 748:
    #                 a = 1
    #             if value != 0:
    #                 found_bigger = False
    #                 neighs = [[0, -1, 0], [-1, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 0], [-1, 1, 0], [1, -1, 0], [-1, 1, 0]]
    #                 for dx, dy, dz in neighs:
    #                     if img[z + dz][y + dy][x + dx] >= value:
    #                         found_bigger = True
    #                 if not found_bigger:
    #                     img[z][y][x] = 300.0
    img_skele = thin(img)

    imwrite("TEST_SKELE.tif", data=img_skele)
