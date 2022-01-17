import datetime

from numpy import uint8, ndarray, zeros
from tifffile.tifffile import imsave
from cell import Cell, CellsStore, DistancesToCells, DistMatrix, ImageSize, PixelNativeList
from img_processing import read_cells
from distance_calculating import calculate_all_mutual_distances, get_border_pixels_between_cells

def print_distances_from_cell(dist : DistancesToCells):
    for d in sorted(dist):
        print(f" -> after {d} pixels is cell id {dist[d]}")

def write_boundaries(pixels: PixelNativeList, label: int, img: ndarray):
    for x,y,z in pixels:
        img[z][y][x] = label


def main():
    t1 = datetime.datetime.now()
    print("Pre-processing image")
    cells: CellsStore = read_cells('./data/masks_3D_small.tif')
    for key in sorted(cells.keys()):
        print(cells[key])

    t2 = datetime.datetime.now()
    print(t2-t1)

    print("Calculating distances")
    distances: DistMatrix = calculate_all_mutual_distances(cells)
    print(datetime.datetime.now()-t2)

    # REPORTING
    refCellLabel = 21
    print(f"distance from cell id {refCellLabel}:")
    print_distances_from_cell(distances[refCellLabel])

    # SHOWING
    otherCellLabel = 36
    rl, ol = get_border_pixels_between_cells(cells[refCellLabel], cells[otherCellLabel])
    img = zeros((100,200,250), dtype=uint8)
    write_boundaries(rl,refCellLabel,img)
    write_boundaries(ol,otherCellLabel,img)
    imsave(f"border_{refCellLabel}-{otherCellLabel}.tif", data=img)

if __name__ == "__main__":
    main()
