from cell import Cell
from img_processing import read_cells


def main():
    cells: dict[int, Cell] = read_cells()
    for cell in cells.values():
        print(cell)
