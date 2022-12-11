import time

from cells.priority import centroid_distance_priority
from cells.processing.distance_calculating import calculate_mutual_distances
from cells.processing.img_processing import read_cells
from cells.project_types import CellsStore
from cells.config import CFG
import os
from fnmatch import fnmatch


def main():
    iterate_over_all_images()


def iterate_over_all_images():
    root = './data'
    pattern = "*.tif"
    cells_amount =[]
    cells_size = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            if fnmatch(name, pattern):
                cells = read_cells(os.path.join(path, name), bbox_border=False)

                print(f"Image '{name}': ")


def run_print_with_config():
    if CFG["method"] == "bbox":
        CFG.precise, precise_old = True, CFG.precise
        print_distance_map(bbox_border=True)
        CFG.precise = precise_old
    else:
        print_distance_map(bbox_border=False)
def print_distance_map(bbox_border=False):
    t0 = time.time()
    cells: CellsStore = read_cells('./data/PhC-C2DL-PSC/01_ST/SEG/man_seg000_2D.tif', bbox_border=bbox_border)
    t1 = time.time()
    # print("started voronoi")
    # compute_voronoi_diagram(cells)
    # print(time.time() - t1)
    priorities = centroid_distance_priority.calculate_priorities(cells)
    t2 = time.time()
    distances = calculate_mutual_distances(cells, priorities)
    t3 = time.time()
    print(f"read: {(t1 - t0)}s, priorities: {(t2 - t1)}s, distances: {(t3 - t2)}s")
    for key in sorted(list(distances.keys())):
        dist = distances[key].items()
        dist = list(map(lambda x: (x[1], x[0]), dist))
        dist.sort()
        dist = list(map(lambda x: (x[1], x[0]), dist))
        print(f"{key}: {dist[0:10]}  {len(dist)}")
    if CFG["data_list"]:
        print(sum(CFG["data_list"]) / len(CFG["data_list"]))


if __name__ == "__main__":
    main()
