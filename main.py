import datetime
from typing import Tuple

from cell import Cell
from img_processing import read_cells


def main():
    cells: dict[int, Cell] = read_cells()
    distances: list[dict[int, Tuple[int, int]]] = []
    for cell in cells.values():
        print(cell)


if __name__ == "__main__":
    main()
