from cells.config import CFG
from cells.processing import border_distance
from cells.project_types import CellPriorityList, DistMatrix, CellsStore, Label, CellPriorityMatrix, CellsToDistances


def calculate_mutual_distances(cells: CellsStore, cell_priority_matrix: CellPriorityMatrix):
    """
    Return distance matrix with format: { cell_label : [{cell_label : (distance, energy)},...] }
    If priority matrix is present - distance matrix won't be full, it will be limited only to
    """
    distances: DistMatrix = {}
    for label in cells.keys():
        cell_priority_list = []
        if cell_priority_matrix is not None:
            # Round to higher number to take at least 1 more cell if limiting coefficient != 1
            limit_to = round(CFG["closest_count"] * CFG["limiting_coefficient"] + 0.5)
            cell_priority_list = cell_priority_matrix[label][:limit_to]
        distance_to_other_cells(cells, label, distances, cell_priority_list)
    return distances


def distance_to_other_cells(cells: CellsStore, ref_label: Label, distances: DistMatrix,
                            cell_priority_list: CellPriorityList) -> None:
    """
    Fill distance matrix with distances from ref_cell to others.
    If priorities are set - will fill distances only to cells from list
    """
    distances[ref_label]: CellsToDistances = {}
    for label, cell in cells.items():
        # don't store the distance to itself
        if label == ref_label:
            continue
        # don't recompute computed distances
        if label in distances and ref_label in distances[label]:
            distances[ref_label][label] = distances[label][ref_label]
            continue
        # if priority list is present - compute distance only to cells from it
        if cell_priority_list is not [] and label not in cell_priority_list:
            continue
        dist = border_distance.distance_between_cells(cells[ref_label], cell)
        distances[ref_label][label] = dist
