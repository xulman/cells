from math import sqrt
from numba import jit
from numba.typed import List
from cell import Cell, CellsStore, Coords, PixelList, DistancesToCells, DistMatrix
from utils import distance, distance_sq

def get_border_pixels_between_cells(fst: Cell, snd: Cell) -> tuple[PixelList, PixelList]:
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
    return fst_border, snd_border


def get_full_border_pixels_between_cells(fst: Cell, snd: Cell) -> tuple[PixelList, PixelList]:
    return fst.surface_pixels, snd.surface_pixels


def distance_between_cells(fst: Cell, snd: Cell) -> int:
    centroid_distance = distance(fst.centroid, snd.centroid)

    fst_border, snd_border = get_border_pixels_between_cells(fst, snd)
    min_distance = distance_between_contours(fst_border, snd_border, centroid_distance)

    #comparison test:
    optCalcs = len(fst_border)*len(snd_border)
    gtCalcs  = len(fst.surface_pixels)*len(snd.surface_pixels)
    print(f"{fst.label}-{snd.label}: {optCalcs} rounds for optimized version")
    print(f"{fst.label}-{snd.label}: {gtCalcs} rounds for GT")
    print(f"{fst.label}-{snd.label}: reduction to {100*optCalcs/gtCalcs} % of GT")
    #
    gt_min_distance = distance_between_contours(fst.surface_pixels, snd.surface_pixels, centroid_distance)
    print(f"{fst.label}-{snd.label}: dist diff: {min_distance-gt_min_distance} pixels")

    return round(min_distance)


@jit
def distance_between_contours(fst_border: list[Coords], snd_border: list[Coords], centroid_distance):
    min_distance = centroid_distance
    for fst_pixel in fst_border[::3]:
        for snd_pixel in snd_border[::3]:
            dist = distance(fst_pixel, snd_pixel)
            if dist < min_distance:
                min_distance = dist
    return min_distance

@jit
def distance_between_contours_sq(fst_border: list[Coords], snd_border: list[Coords], centroid_distance):
    min_distance_sq = centroid_distance*centroid_distance
    for fst_pixel in fst_border[::3]:
        for snd_pixel in snd_border[::3]:
            dist_sq = distance_sq(fst_pixel, snd_pixel)
            if dist_sq < min_distance_sq:
                min_distance_sq = dist_sq
    return sqrt(min_distance_sq)


def distance_to_other_cells(ref_cell: Cell, cells: CellsStore, distances: DistMatrix) -> None:
    distances[ref_cell.label]: DistancesToCells = {}
    for label, cell in cells.items():
        if label == ref_cell.label: # don't store the distance to itself
            continue
        if label in distances: # was computed before?
            for dist,id in distances[label].items():
                if id == ref_cell.label:
                    distances[ref_cell.label][dist] = label
            continue
        distances[ref_cell.label][ distance_between_cells(ref_cell, cell) ] = label


def calculate_all_mutual_distances(cells: CellsStore):
    distances: DistMatrix = {}
    for cell in cells.values():
        distance_to_other_cells(cell, cells, distances)
    return distances
