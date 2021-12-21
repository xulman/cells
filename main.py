import datetime
import time
from typing import Tuple

from cell import Cell
from img_processing import read_cells


def main():
    was = datetime.datetime.now()
    cells: dict[int, Cell] = read_cells()
    print(datetime.datetime.now() - was)
    distances: list[dict[int, Tuple[int, int]]] = []
    for cell in cells.values():
        print(cell)


if __name__ == "__main__":
    main()
