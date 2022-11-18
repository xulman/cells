from cells.processing.utils import distance
from cells.types import CellsStore, CellPriorityMatrix


def calculate_priorities(cells: CellsStore):
    priorities: CellPriorityMatrix = {}

    for current_label in cells.keys():
        current_centroid = cells[current_label].centroid
        # Create sorted list with format [(distance_from_current, label), ...]
        distances_from_current = []
        for checked_label in cells.keys():
            if checked_label == current_label:
                continue
            checked_centroid = cells[checked_label].centroid
            distances_from_current.append((distance(current_centroid, checked_centroid), checked_label))
        # Tuples are being sorted by first element and if they are equal - by the second. This will sort by distance.
        distances_from_current.sort()
        # Extract only labels
        priorities[current_label] = list(map(lambda x: x[1],  distances_from_current))
    return priorities
# NOTE: this could be optimised by re-using calculated distances, but it seems unnecessary as it wouldn't save that much computation time.