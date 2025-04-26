import math

import pygame

from utils import distancia


class Lobo:
    VELOCIDADE = 3.5

    def __init__(self, x, y, img, ambiente):
        self.x = x
        self.y = y
        self.img = img
        self.ambiente = ambiente
        self.vivo = True
        self.fitness = 0

    def desenhar(self, screen):
        screen.blit(self.img, (self.x, self.y))

    def mover(self, output):
        if not self.vivo:
            return

        dx = output[0] * self.VELOCIDADE
        dy = output[1] * self.VELOCIDADE
        novo_x = self.x + dx
        novo_y = self.y + dy

        if self.ambiente.posicao_valida(novo_x, novo_y):
            self.x = novo_x
            self.y = novo_y

    def calcular_inputs(self, coelhos):
        if not coelhos:
            return [0, 0]

        coelho_mais_proximo = min(
            coelhos, key=lambda coelho: distancia(self.x, self.y, coelho.x, coelho.y)
        )
        dx = coelho_mais_proximo.x - self.x
        dy = coelho_mais_proximo.y - self.y

        dist = distancia(self.x, self.y, coelho_mais_proximo.x, coelho_mais_proximo.y)
        return [dx / (dist + 1e-5), dy / (dist + 1e-5)]
