from ctypes import ArgumentError
from case_study import CaseStudy
from cell import CellsToDistancesWithEnergies, DistMatrix

def count_distances_outside_tolerance_treshold(test: CellsToDistancesWithEnergies, ref: CellsToDistancesWithEnergies, tolerance: int):
    if len(test) != len(ref):
        print(f"lengths mismatch: {len(test)} vs. {len(ref)} for test vs. ref data")

    cnt: int = 0
    for cell_id in ref:
        if cell_id not in test:
            print(f"cell {cell_id} is missing in test data")
            raise ArgumentError(f"missing {cell_id} in test data")

        cnt = cnt if abs( ref[cell_id][0] - test[cell_id][0] ) <= tolerance else cnt+1

    return cnt


def count_distances_outside_tolerance_treshold__matrix(test: DistMatrix, ref: DistMatrix, tolerance: int):
    cnt = 0
    for cell_id in ref:
        if cell_id not in test:
            print(f"cell {cell_id} is missing in test data")
            raise ArgumentError(f"missing {cell_id} in test data")

        cnt += count_distances_outside_tolerance_treshold(test[cell_id], ref[cell_id], tolerance)
    return cnt


def count_distances_outside_tolerance_treshold__study(case_study: CaseStudy, tolerance: int):
    return count_distances_outside_tolerance_treshold__matrix(case_study.distances, case_study.distances_gt, tolerance)