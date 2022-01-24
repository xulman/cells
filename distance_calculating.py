from math import sqrt

from numba import jit
from numba.typed import List

from cell import Cell, CellsStore, PixelNumbaList, DistMatrix, DistancesToCellsWithEnergies, CellAndEnergy
from utils import distance, distance_sq


def get_border_pixels_between_cells(fst: Cell, snd: Cell) -> tuple[PixelNumbaList, PixelNumbaList]:
    # If cell #1 is less round - farther pixels of cell #2 should be taken, and other way
    centroid_distance = distance(fst.centroid, snd.centroid)
    fst_border: PixelNumbaList = List()
    snd_border: PixelNumbaList = List()
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
    return fst_border, snd_border


def get_full_border_pixels_between_cells(fst: Cell, snd: Cell) -> tuple[PixelNumbaList, PixelNumbaList]:
    # re-packs into Numba list (to avoid Numba compiler warnings...)
    if fst.surface_pixels_numba is None:
        fst.surface_pixels_numba = List()
        [fst.surface_pixels_numba.append(x) for x in fst.surface_pixels]
    if snd.surface_pixels_numba is None:
        snd.surface_pixels_numba = List()
        [snd.surface_pixels_numba.append(x) for x in snd.surface_pixels]
    return fst.surface_pixels_numba, snd.surface_pixels_numba


def distance_between_cells(fst: Cell, snd: Cell) -> int:
    centroid_distance = distance(fst.centroid, snd.centroid)

    fst_border, snd_border = get_border_pixels_between_cells(fst, snd)
    min_distance,E = distance_between_contours(fst_border, snd_border, centroid_distance)

    # comparison test:
    optCalcs = len(fst_border) * len(snd_border)
    gtCalcs = len(fst.surface_pixels) * len(snd.surface_pixels)
    print(f"{fst.label}-{snd.label}: {optCalcs} rounds for optimized version")
    print(f"{fst.label}-{snd.label}: {gtCalcs} rounds for GT")
    print(f"{fst.label}-{snd.label}: reduction to {100 * optCalcs / gtCalcs} % of GT")
    #
    fst_border_full, snd_border_full = get_full_border_pixels_between_cells(fst, snd)
    print(f"dist between cells {fst.label}-{snd.label}:")
    print(f" -> considering pixels {len(fst_border_full)} and {len(snd_border_full)}")
    gt_min_distance,gt_E = distance_between_contours(fst_border_full, snd_border_full, centroid_distance)
    print(f"{fst.label}-{snd.label}: dist diff: {min_distance - gt_min_distance} pixels")

    return round(min_distance)


def distance_opt_between_cells(fst: Cell, snd: Cell) -> CellAndEnergy:
    centroid_distance = distance(fst.centroid, snd.centroid)
    fst_border, snd_border = get_border_pixels_between_cells(fst, snd)
    opt_min_distance,E = distance_between_contours(fst_border, snd_border, centroid_distance)
    return round(opt_min_distance),E


def distance_gt_between_cells(fst: Cell, snd: Cell) -> CellAndEnergy:
    centroid_distance = distance(fst.centroid, snd.centroid)
    fst_border, snd_border = get_full_border_pixels_between_cells(fst, snd)
    gt_min_distance,E = distance_between_contours(fst_border, snd_border, centroid_distance)
    return round(gt_min_distance),E


@jit
def distance_between_contours(fst_border: PixelNumbaList, snd_border: PixelNumbaList, centroid_distance, skip_step: int = 3) -> CellAndEnergy:
    min_distance = centroid_distance
    fst_b = fst_border[::skip_step]
    snd_b = snd_border[::skip_step]
    for fst_pixel in fst_b:
        for snd_pixel in snd_b:
            dist = distance(fst_pixel, snd_pixel)
            if dist < min_distance:
                min_distance = dist
    return min_distance, len(fst_b)*len(snd_b)


@jit
def distance_between_contours_sq(fst_border: PixelNumbaList, snd_border: PixelNumbaList, centroid_distance, skip_step: int = 3) -> CellAndEnergy:
    min_distance_sq = centroid_distance * centroid_distance
    fst_b = fst_border[::skip_step]
    snd_b = snd_border[::skip_step]
    for fst_pixel in fst_b:
        for snd_pixel in snd_b:
            dist_sq = distance_sq(fst_pixel, snd_pixel)
            if dist_sq < min_distance_sq:
                min_distance_sq = dist_sq
    return sqrt(min_distance_sq), len(fst_b)*len(snd_b)


def distance_to_other_cells(ref_cell: Cell, cells: CellsStore, distances: DistMatrix, do_full_gt: bool = False) -> None:
    distances[ref_cell.label]: DistancesToCellsWithEnergies = {}
    for label, cell in cells.items():
        if label == ref_cell.label:  # don't store the distance to itself
            continue
        if label in distances:  # was computed before?
            for dist, cell_and_energy in distances[label].items():
                if cell_and_energy[0] == ref_cell.label:
                    distances[ref_cell.label][dist] = (label,cell_and_energy[1])
            continue
        dist,E = distance_opt_between_cells(ref_cell, cell) if not do_full_gt \
            else distance_gt_between_cells(ref_cell, cell)
        distances[ref_cell.label][dist] = (label,E)


def calculate_all_mutual_distances(cells: CellsStore, do_full_gt: bool = False):
    distances: DistMatrix = {}
    for cell in cells.values():
        distance_to_other_cells(cell, cells, distances, do_full_gt)
    return distances
