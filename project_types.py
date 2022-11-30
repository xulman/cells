from numba.typed import List
from cells.processing.cell import Cell

ImageSize = tuple[int, int, int]

Coords = tuple[int, int, int]
PixelNativeList = list[Coords]
PixelNumbaList = List[Coords]
Image = list[list[list[int]]]

Label = int
Distance = int
CellsToDistances = dict[Label, Distance]  # otherCellId -> distance
DistMatrix = dict[Label, CellsToDistances]  # cell -> (otherCell -> distance,)
CellsStore = dict[int, Cell]

CellPriorityList = list[Label]
CellPriorityMatrix = dict[Label, CellPriorityList]

Vertex = int
Weight = int
Edge = tuple[Vertex, Vertex, Weight]
Graph = tuple[list[Vertex], list[Edge]]
