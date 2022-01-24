from pickle import Pickler, Unpickler
from typing import Optional
from cell import CellsStore, DistMatrix, ImageSize

class CaseStudy:
    def __init__(self, imageFileName: str, imageSize: ImageSize):
        self.imageFile = imageFileName
        self.imageSize = ImageSize
        p_from = imageFileName.rfind('/')+1
        p_end = imageFileName.rfind('.')
        self.pickleFile = imageFileName[ p_from:p_end ]+".dat"

        self.distances_gt: DistMatrix = None
        self.distances: DistMatrix = None

class Payload:
    def __init__(self) -> None:
        self.case_study: CaseStudy = None
        self.cells: CellsStore = None

def store_case_study(case_study: CaseStudy, cells: CellsStore):
    print(f"Storing case study into {case_study.pickleFile}")
    with open(case_study.pickleFile,"wb") as file:
        p = Pickler(file)
        data = Payload()
        data.case_study = case_study
        data.cells = cells
        p.dump(data)


def load_case_study(reference_case_study: CaseStudy) -> Optional[tuple[CaseStudy,CellsStore]]:
    print(f"Loading case study from {reference_case_study.pickleFile}")
    with open(reference_case_study.pickleFile,"rb") as file:
        p = Unpickler(file)
        data: Payload = p.load()
        return data.case_study, data.cells