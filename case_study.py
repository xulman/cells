from pickle import Pickler, Unpickler
from typing import Optional
from cell import CellsStore, DistMatrix, ImageSize
from distance_calculating import calculate_all_mutual_distances
from img_processing import read_cells

class CaseStudy:
    def __init__(self, imageFileName: str, imageSize: ImageSize):
        self.imageFile = imageFileName
        self.imageSize = ImageSize
        p_from = imageFileName.rfind('/')+1
        p_end = imageFileName.rfind('.')
        self.pickleFile = imageFileName[ p_from:p_end ]+".dat"

        self.cells: CellsStore = None
        self.distances_gt: DistMatrix = None
        self.distances: DistMatrix = None

    def calculate_cells(self):
        print(f"Calculating pre-processing data for {self.imageFile}")
        self.cells = read_cells(self.imageFile)

    def calculate_opt_distances(self):
        if self.cells is None:
            self.calculate_cells()
        self.distances = calculate_all_mutual_distances(self.cells,do_full_gt=False)

    def calculate_gt_distances(self):
        if self.cells is None:
            self.calculate_cells()
        self.distances_gt = calculate_all_mutual_distances(self.cells,do_full_gt=True)


def store_case_study(case_study: CaseStudy):
    print(f"Storing case study into {case_study.pickleFile}")
    with open(case_study.pickleFile,"wb") as file:
        Pickler(file).dump(case_study)


def load_case_study(reference_case_study: CaseStudy) -> Optional[CaseStudy]:
    print(f"Loading case study from {reference_case_study.pickleFile}")
    with open(reference_case_study.pickleFile,"rb") as file:
        return Unpickler(file).load()