from math import sqrt
from numba import jit
from cell import Coords

@jit
def distance(fst: Coords, snd: Coords) -> float:
    return sqrt((fst[0]-snd[0]) ** 2 + (fst[1]-snd[1]) ** 2 + (fst[2]-snd[2]) ** 2)

@jit
def distance_sq(fst: Coords, snd: Coords) -> float:
    return (fst[0]-snd[0]) ** 2 + (fst[1]-snd[1]) ** 2 + (fst[2]-snd[2]) ** 2
