import numpy as np
from matplotlib import pyplot as plt
from skimage.feature import peak_local_max
from skimage.segmentation import watershed
from tifffile import imwrite

from cells.project_types import Graph, Image
from scipy import ndimage
from skimage.morphology import skeletonize, thin


def create_distance_graph(image: Image) -> Graph:
    image_base = np.array(image[0])
    size = len(image[0][0]), len(image[0]), len(image)
    for z in range(size[2]):
        for y in range(size[1]):
            for x in range(size[0]):
                value = image[z][y][x]
                if value != 0:
                    image[z][y][x] = 0
                else:
                    image[z][y][x] = 1
    image = np.array(image[0])

    distance = ndimage.distance_transform_edt(image, return_distances=True)
    coords = peak_local_max(-distance, footprint=np.ones((3, 3)), labels=image)
    mask = np.zeros(distance.shape, dtype=bool)
    mask[tuple(coords.T)] = True
    markers, _ = ndimage.label(mask)

    labels = watershed(distance, markers, mask=image)
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
    fig, axes = plt.subplots(ncols=3, figsize=(9, 3), sharex=True, sharey=True)
    ax = axes.ravel()

    ax[0].imshow(image, cmap=plt.cm.gray)
    ax[0].set_title('Overlapping objects')
    ax[1].imshow(-distance, cmap=plt.cm.gray)
    ax[1].set_title('Distances')
    ax[2].imshow(labels, cmap=plt.cm.nipy_spectral)
    ax[2].set_title('Separated objects')


    for a in ax:
        a.set_axis_off()

    fig.tight_layout()
    plt.show()

    #imwrite("TEST_SKELE.tif", data=img_skele)
