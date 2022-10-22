from numba.typed import List
from cells.processing.cell import Cell

ImageSize = tuple[int, int, int]

Coords = tuple[int, int, int]
PixelNativeList = list[Coords]
PixelNumbaList = List[Coords]

Label = int
Distance = int
CellsToDistances = dict[Label, Distance]  # otherCellId -> distance
DistMatrix = dict[Label, CellsToDistances]  # cell -> (otherCell -> distance,)
CellsStore = dict[int, Cell]

CellPriorityList = list[Label]
CellPriorityMatrix = dict[Label, CellPriorityList]

