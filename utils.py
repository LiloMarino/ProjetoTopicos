import math
import os

ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets")


def distancia(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
