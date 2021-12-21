import datetime

from cell import Cell
from img_processing import read_cells
from distance_calculating import calculate_distances


def main():
    was = datetime.datetime.now()
    print("Processing image")
    cells: dict[int, Cell] = read_cells('./data/masks_3D.tif')
    # for key in cells.keys():
    #     print(cells[key])
    distances: dict[int, dict[int, int]]
    print("Calculating distances")
    distances = calculate_distances(cells)
    # for key in distances.keys():
    #     print(distances[key])
    print(datetime.datetime.now()-was)


if __name__ == "__main__":
    main()
