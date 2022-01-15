import datetime
from cell import Cell, CellsStore, DistancesToCells, DistMatrix
from img_processing import read_cells
from distance_calculating import calculate_all_mutual_distances

def printDistancesFromCell(dist : DistancesToCells):
    for d in sorted(dist):
        print(f" -> after {d} pixels is cell id {dist[d]}")

def main():
    t1 = datetime.datetime.now()
    print("Pre-processing image")
    cells: CellsStore = read_cells('./data/masks_3D.tif')
    for key in sorted(cells.keys()):
        print(cells[key])

    t2 = datetime.datetime.now()
    print(t2-t1)

    print("Calculating distances")
    distances: DistMatrix = calculate_all_mutual_distances(cells)
    print(datetime.datetime.now()-t2)

    refCellLabel = 25
    print(f"distance from cell id {refCellLabel}:")
    printDistancesFromCell(distances[refCellLabel])


if __name__ == "__main__":
    main()
