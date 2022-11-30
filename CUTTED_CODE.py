from cells.config import CFG
from cells.processing.border_distance import border_pixels_between_cells, distance_between_cells
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


# OLD MAIN
    import datetime

    from numpy import uint8, ndarray, zeros
    from tifffile.tifffile import imwrite
    from case_study import CaseStudy, load_case_study, store_case_study

    from cells.processing.cell import CellsStore, CellsToDistancesWithEnergies, DistMatrix, PixelNativeList
    from cells.processing.border_distance import calculate_mutual_distances, border_pixels_between_cells
    from error_measures import count_distances_outside_tolerance_treshold, count_distances_outside_tolerance_treshold__study, count_rank_mismatches
    from cells.processing.img_processing import read_cells

    def print_distances_from_cell(dist: CellsToDistancesWithEnergies):
        for d in sorted(dist, key=lambda k: dist[k][0]):
            print(f" -> after {dist[d][0]} pixels is cell id {d}, measurement price {dist[d][1]}")

    def print_distances_matrix(dists: DistMatrix):
        for cell_id,dist in dists.items():
            print(f"Distances from cell {cell_id} to other {len(dist)} cells:")
            print_distances_from_cell(dist)


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
        distances: DistMatrix = calculate_mutual_distances(cells)
        print(datetime.datetime.now() - t2)

        # REPORTING
        refCellLabel = 21
        print(f"distance from cell id {refCellLabel}:")
        print_distances_from_cell(distances[refCellLabel])

        # SHOWING
        otherCellLabel = 36
        rl, ol = border_pixels_between_cells(cells[refCellLabel], cells[otherCellLabel])
        img = zeros((100, 200, 300), dtype=uint8)
        write_boundaries(rl, refCellLabel, img)
        write_boundaries(ol, otherCellLabel, img)
        imwrite(f"border_{refCellLabel}-{otherCellLabel}.tif", data=img)


    def create_case_study():
        #return CaseStudy('./data/masks_2D.tif',   [1,922,922])
        #return CaseStudy('./data/masks_3D.tif', [100,922,922])
        #return CaseStudy('./data/masks_3D_small.tif', [100,200,250])

        return CaseStudy('./data/fake_cells_2D.tif',  [1,400,512])
        #return CaseStudy('./data/fake_cells_3D.tif', [21,400,512])


    def main_save():
        cs = create_case_study()

        # "create" data
        cs.calculate_cells()
        for key in sorted(cs.cells.keys()):
            print(cs.cells[key])
        cs.calculate_opt_distances()
        print_distances_from_cell(cs.distances[12])

        store_case_study(cs)


    def main_load():
        # restore data structures from pre-saved data rather than computing anew
        cs = load_case_study( create_case_study() )

        # test "restored" data
        for key in sorted(cs.cells.keys()):
            print(cs.cells[key])
        print_distances_from_cell(cs.distances[12])

        # try to calcuate distance again
        #cs.distances = calculate_all_mutual_distances(cs.cells,do_full_gt=False)
        cs.calculate_opt_distances()
        print_distances_from_cell(cs.distances[12])


    def main():
        cs: CaseStudy = load_case_study( create_case_study() )

        for key in sorted(cs.cells.keys()):
            print(cs.cells[key])

        img = zeros(cs.imageSize, dtype=uint8)
        for cell_id in cs.cells.keys():
            cs.cells[cell_id].visualize(img)

        fileName = f"augmented_cells_for_{cs.imageFile[cs.imageFile.rfind('/')+1:]}"
        print(f"Storing image: {fileName}")
        imwrite(fileName, data=img)

    def main_evaluating():
        cs: CaseStudy = load_case_study(create_case_study())
        cs.calculate_opt_distances()  # adds the missing calculation...

        tolerance_thres = 0
        for ref_cell in cs.cells:
            print(f"Reference distances from the cell {ref_cell}:")
            print_distances_from_cell(cs.distances_gt[ref_cell])
            print(f"Tested distances from the cell {ref_cell}:")
            print_distances_from_cell(cs.distances[ref_cell])

            print(f"number of dist. diffences (given the tolerance of {tolerance_thres} pixels) is "\
                f"{count_distances_outside_tolerance_treshold(cs.distances[ref_cell],cs.distances_gt[ref_cell],tolerance=tolerance_thres)}")
            print(f"number of rank diffences is "\
                f"{count_rank_mismatches(cs.distances[ref_cell],cs.distances_gt[ref_cell])}")
            print("-------------------------")
        print(f"total number of issues is {count_distances_outside_tolerance_treshold__study(cs,tolerance=tolerance_thres)}")

    if __name__ == "__main__":
        #main()
        main_main()
        #main_save(\)"
        #main_load()
        #main_evaluating()

#OLD MAIN END