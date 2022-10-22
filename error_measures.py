from ctypes import ArgumentError
from case_study import CaseStudy
from cells.processing.cell import CellsToDistancesWithEnergies, DistMatrix

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


def count_rank_mismatches(test: CellsToDistancesWithEnergies, ref: CellsToDistancesWithEnergies):
    if len(test) != len(ref):
        print(f"lengths mismatch: {len(test)} vs. {len(ref)} for test vs. ref data")

    test_sorted = list( sorted(test, key=lambda k: test[k][0]) )
    ref_sorted = list( sorted(ref, key=lambda k: ref[k][0]) )

    cnt: int = 0
    for idx,cell_id in enumerate(ref_sorted):
        if cell_id not in test:
            print(f"cell {cell_id} is missing in test data")
            raise ArgumentError(f"missing {cell_id} in test data")

        cnt = cnt if ref_sorted[idx] == test_sorted[idx] else cnt+1

    return cnt


def count_rank_mismatches__matrix(test: DistMatrix, ref: DistMatrix):
    cnt = 0
    for cell_id in ref:
        if cell_id not in test:
            print(f"cell {cell_id} is missing in test data")
            raise ArgumentError(f"missing {cell_id} in test data")

        cnt += count_rank_mismatches(test[cell_id], ref[cell_id])
    return cnt


def count_rank_mismatches__study(case_study: CaseStudy):
    return count_rank_mismatches__matrix(case_study.distances, case_study.distances_gt)
