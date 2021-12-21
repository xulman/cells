import datetime

from cell import Cell
from img_processing import read_cells
from distance_calculating import distance_to_each_cell


def main():
    cells: dict[int, Cell] = read_cells()
    distances: dict[int, dict[int, int]] = {}
    was = datetime.datetime.now()
    print(distance_to_each_cell(cells[25], cells))
    print(datetime.datetime.now()-was)


if __name__ == "__main__":
    main()
