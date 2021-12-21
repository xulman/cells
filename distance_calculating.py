from cell import Cell, Coords

from utils import distance


def distance_between_cells(fst: Cell, snd: Cell) -> int:
    # If cell #1 is less round - farther pixels of cell #2 should be taken, and other way
    centroid_distance = distance(fst.centroid, snd.centroid)
    fst_border: list[Coords] = []
    snd_border: list[Coords] = []
    fst_compare_distance = centroid_distance - fst.avg_radius * (1 / (fst.roundness + 0.1) ** 2)
    snd_compare_distance = centroid_distance - snd.avg_radius * (1 / (snd.roundness + 0.1) ** 2)

    # cutting pixels that are too far to be closest
    for pixel in fst.surface_pixels:
        if distance(pixel, snd.centroid) <= fst_compare_distance:
            fst_border.append(pixel)
    for pixel in snd.surface_pixels:
        if distance(pixel, fst.centroid) <= snd_compare_distance:
            snd_border.append(pixel)

    print(f"fst border: {len(fst_border)}, snd border {len(snd_border)}")
    min_distance = centroid_distance
    for fst_pixel in fst_border[::3]:
        for snd_pixel in snd_border[::3]:
            dist = distance(fst_pixel, snd_pixel)
            if dist < min_distance:
                min_distance = dist

    return round(min_distance)


def distance_to_each_cell(main_cell: Cell, cells: dict[int, Cell]) -> dict[int, int]:
    distances: dict[int, int] = {}
    for label, cell in cells.items():
        if label == main_cell.label:
            continue
        distances[label] = distance_between_cells(main_cell, cell)
    return distances
