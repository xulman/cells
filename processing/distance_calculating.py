from numba import jit
from numba.typed import List

from cells.processing.cell import Cell, CellsStore, PixelNumbaList, DistMatrix, CellsToDistances, Distance
from utils import distance
from cells.config import CFG


def calculate_all_mutual_distances(cells: CellsStore):
    """
    Return distance matrix with format: { cell_label : [{cell_label : (distance, energy)},...] }
    """
    distances: DistMatrix = {}
    for cell in cells.values():
        distance_to_other_cells(cells, cell, distances)
    return distances


def distance_to_other_cells(cells: CellsStore, ref_cell: Cell, distances: DistMatrix) -> None:
    """
    Fill distance matrix with distances from ref_cell to others.
    """
    distances[ref_cell.label]: CellsToDistances = {}
    for label, cell in cells.items():
        if label == ref_cell.label:  # don't store the distance to itself
            continue
        if label in distances:  # was computed before?
            distances[ref_cell.label][label] = distances[label][ref_cell.label]
            continue
        dist = distance_between_cells(ref_cell, cell)
        distances[ref_cell.label][label] = dist


def distance_between_cells(fst: Cell, snd: Cell) -> Distance:
    """
    Compute distance and energy between two cells using optimal strategy
    """
    centroid_distance = distance(fst.centroid, snd.centroid)
    fst_border, snd_border = border_pixels_between_cells(fst, snd)
    min_distance = distance_between_borders(fst_border, snd_border, centroid_distance)
    return round(min_distance)


def border_pixels_between_cells(fst: Cell, snd: Cell) -> tuple[PixelNumbaList, PixelNumbaList]:
    """
    Get arrays of pixels that will be then used to calculate distance.
    """
    if CFG["precise"]:
        # re-packs into Numba list (to avoid Numba compiler warnings...)
        if fst.surface_pixels_numba is None:
            fst.surface_pixels_numba = List()
            [fst.surface_pixels_numba.append(x) for x in fst.surface_pixels]
        if snd.surface_pixels_numba is None:
            snd.surface_pixels_numba = List()
            [snd.surface_pixels_numba.append(x) for x in snd.surface_pixels]
        return fst.surface_pixels_numba, snd.surface_pixels_numba
    else:
        # If cell #1 is less round - farther pixels of cell #2 should be taken, and other way
        centroid_distance = distance(fst.centroid, snd.centroid)
        fst_border: PixelNumbaList = List()
        snd_border: PixelNumbaList = List()
        # magic happens here
        modifier = 0.15 if centroid_distance > (fst.avg_radius * 2) and centroid_distance > (
                    snd.avg_radius * 2) else 0.30
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
        return fst_border, snd_border


@jit
def distance_between_borders(fst_border: PixelNumbaList, snd_border: PixelNumbaList, centroid_distance) -> Distance:
    """
    Calculates distance between two selected borders.
    """
    skip_step = CFG["skip_step"]
    min_distance = centroid_distance
    fst_b = fst_border[::skip_step]
    snd_b = snd_border[::skip_step]
    for fst_pixel in fst_b:
        for snd_pixel in snd_b:
            dist = distance(fst_pixel, snd_pixel)
            if dist < min_distance:
                min_distance = dist
    return min_distance
