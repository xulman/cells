import math

Coords = tuple[int, int, int]


def distance(fst: Coords, snd: Coords) -> float:
    return math.sqrt((fst[0]-snd[0]) ** 2 + (fst[1]-snd[1]) ** 2 + (fst[2]-snd[2]) ** 2)
