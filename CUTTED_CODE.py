from cells.config import CFG
from cells.processing.distance_calculating import border_pixels_between_cells, distance_between_cells
from copy import copy


def log_difference_between_optimal_and_precise():
    """
    If this function would be needed - it needs rework:
    Using local config - optimal and precise borders and distances should be calculated
    and then compared.
    """
    optCalcs = len(fst_border) * len(snd_border)
    gtCalcs = len(fst.surface_pixels) * len(snd.surface_pixels)
    print(f"{fst.label}-{snd.label}: {optCalcs} rounds for optimized version")
    print(f"{fst.label}-{snd.label}: {gtCalcs} rounds for GT")
    print(f"{fst.label}-{snd.label}: reduction to {100 * optCalcs / gtCalcs} % of GT")
    #
    fst_border_full, snd_border_full = get_full_border_pixels_between_cells(fst, snd)
    print(f"dist between cells {fst.label}-{snd.label}:")
    print(f" -> considering pixels {len(fst_border_full)} and {len(snd_border_full)}")
    gt_min_distance, gt_E = distance_between_contours(fst_border_full, snd_border_full, centroid_distance)
    print(f"{fst.label}-{snd.label}: dist diff: {min_distance - gt_min_distance} pixels")