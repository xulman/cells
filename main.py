import datetime

from numpy import uint8, ndarray, zeros
from tifffile.tifffile import imsave
from case_study import CaseStudy, load_case_study, store_case_study

from cell import CellsStore, DistancesToCells, DistMatrix, PixelNativeList
from distance_calculating import calculate_all_mutual_distances, get_border_pixels_between_cells
from img_processing import read_cells


def print_distances_from_cell(dist: DistancesToCells):
    for d in sorted(dist):
        print(f" -> after {d} pixels is cell id {dist[d]}")


def write_boundaries(pixels: PixelNativeList, label: int, img: ndarray):
    for x, y, z in pixels:
        img[z][y][x] = label


def main_main():
    t1 = datetime.datetime.now()
    print("Pre-processing image")
    cells: CellsStore = read_cells('./data/masks_3D.tif')
    for key in sorted(cells.keys()):
        print(cells[key])

    t2 = datetime.datetime.now()
    print(t2 - t1)

    print("Calculating distances")
    distances: DistMatrix = calculate_all_mutual_distances(cells)
    print(datetime.datetime.now() - t2)

    # REPORTING
    refCellLabel = 21
    print(f"distance from cell id {refCellLabel}:")
    print_distances_from_cell(distances[refCellLabel])

    # SHOWING
    otherCellLabel = 36
    rl, ol = get_border_pixels_between_cells(cells[refCellLabel], cells[otherCellLabel])
    img = zeros((100, 200, 300), dtype=uint8)
    write_boundaries(rl, refCellLabel, img)
    write_boundaries(ol, otherCellLabel, img)
    imsave(f"border_{refCellLabel}-{otherCellLabel}.tif", data=img)


def create_case_study():
    #return CaseStudy('./data/masks_2D.tif',   [1,922,922])
    #return CaseStudy('./data/masks_3D.tif', [100,922,922])
    #return CaseStudy('./data/masks_3D_small.tif', [100,200,250])

    return CaseStudy('./data/fake_cells_2D.tif',  [1,400,512])
    #return CaseStudy('./data/fake_cells_3D.tif', [21,400,512])


def main_save():
    cs = create_case_study()

    # "create" data
    cells: CellsStore = read_cells(cs.imageFile)
    for key in sorted(cells.keys()):
        print(cells[key])
    cs.distances = calculate_all_mutual_distances(cells,do_full_gt=False)
    print_distances_from_cell(cs.distances[12])

    store_case_study(cs,cells)


def main_load():
    # restore data structures from pre-saved data rather than computing anew
    cs,cells = load_case_study( create_case_study() )

    # test "restored" data
    for key in sorted(cells.keys()):
        print(cells[key])
    print_distances_from_cell(cs.distances[12])

    # try to calcuate distance again
    cs.distances = calculate_all_mutual_distances(cells,do_full_gt=False)
    print_distances_from_cell(cs.distances[12])


def main():
    cells: CellsStore = read_cells('./data/fake_cells_3D.tif')
    for key in sorted(cells.keys()):
        print(cells[key])

    # img = zeros((21,400,512), dtype=uint8) -- now intentionally 2D for vizu
    img = zeros((1, 400, 512), dtype=uint8)
    for cell_id in cells.keys():
        cells[cell_id].visualize(img)
    imsave(f"cells.tif", data=img)


if __name__ == "__main__":
    #main_main()
    main_save()
    main_load()
