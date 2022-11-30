import time

from cells.priority import centroid_distance_priority
from cells.processing.distance_calculating import calculate_mutual_distances
from cells.processing.img_processing import read_cells
from cells.project_types import CellsStore
from cells.config import CFG


def main():
    if CFG.method == "bbox":
        CFG.precise, precise_old = True, CFG.precise
        print_distance_map(bbox_border=True)
        CFG.precise = precise_old
    else:
        print_distance_map(bbox_border=False)


def print_distance_map(bbox_border=False):
    t0 = time.time()
    cells: CellsStore = read_cells('./data/masks_3D.tif', bbox_border=bbox_border)
    t1 = time.time()
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


if __name__ == "__main__":
    main()
