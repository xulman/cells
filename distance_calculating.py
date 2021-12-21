from numba import jit
from numba.typed import List

from cell import Cell, Coords

from utils import distance


def distance_between_cells(fst: Cell, snd: Cell) -> int:
    # If cell #1 is less round - farther pixels of cell #2 should be taken, and other way
    centroid_distance = distance(fst.centroid, snd.centroid)
    fst_border: list[Coords] = List()
    snd_border: list[Coords] = List()
    # magic happens here
    modifier = 0.15 if centroid_distance > (fst.avg_radius * 2) and centroid_distance > (snd.avg_radius * 2) else 0.30
    fst_compare_distance = centroid_distance - fst.avg_radius * (1 / ((fst.roundness + modifier) ** 3))
    snd_compare_distance = centroid_distance - snd.avg_radius * (1 / ((snd.roundness + modifier) ** 3))

    # cutting pixels that are too far to be closest
    for pixel in fst.surface_pixels:
        if distance(pixel, snd.centroid) <= fst_compare_distance:
            fst_border.append(pixel)
    for pixel in snd.surface_pixels:
        if distance(pixel, fst.centroid) <= snd_compare_distance:
            snd_border.append(pixel)
    # if len(fst_border) < 500 or len(snd_border) < 500:
    #     print(f"{fst.label} border: {len(fst_border)}, {snd.label} border: {len(snd_border)}, distance between {centroid_distance}")
    min_distance = distance_between_borders(fst_border, snd_border, centroid_distance)


    return round(min_distance)


@jit
def distance_between_borders(fst_border: List[Coords], snd_border: List[Coords], centroid_distance):
    min_distance = centroid_distance
    for fst_pixel in fst_border[::3]:
        for snd_pixel in snd_border[::3]:
            dist = distance(fst_pixel, snd_pixel)
            if dist < min_distance:
                min_distance = dist
    return min_distance


def distance_to_each_cell(main_cell: Cell, cells: dict[int, Cell], distances: dict[int, dict[int, int]]) -> None:
    distances[main_cell.label]: dict[int, int] = {}
    for label, cell in cells.items():
        if label == main_cell.label:
            continue
        if label in distances:  # was computed before
            distances[main_cell.label][label] = distances[label][main_cell.label]
            continue
        distances[main_cell.label][label] = distance_between_cells(main_cell, cell)


def calculate_distances(cells: dict[int, Cell]):
    distances: dict[int, dict[int, int]] = {}
    for label, cell in cells.items():
        distance_to_each_cell(cell, cells, distances)
    return distances
