import math


def distancia(x1: float, y1: float, x2: float, y2: float) -> float:
    """Calcula distância euclidiana"""
    return math.hypot(x2 - x1, y2 - y1)
