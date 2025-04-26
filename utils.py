import math


def distancia(x1, y1, x2, y2):
    """Calcula distância euclidiana"""
    return math.hypot(x2 - x1, y2 - y1)


def normalizar(valor, min_valor, max_valor):
    """Normaliza valor para [0,1]"""
    if max_valor - min_valor == 0:
        return 0
    return (valor - min_valor) / (max_valor - min_valor)
