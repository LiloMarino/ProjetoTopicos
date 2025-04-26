import math

import pygame

from utils import distancia


class Coelho:
    VELOCIDADE = 3

    def __init__(self, x, y, img, ambiente):
        self.x = x
        self.y = y
        self.img = img
        self.ambiente = ambiente
        self.vivo = True
        self.tempo_vivo = 0
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

        self.tempo_vivo += 1

    def calcular_inputs(self, lobos):
        if not self.vivo:
            return [0, 0]

        lobo_mais_proximo = min(
            lobos, key=lambda lobo: distancia(self.x, self.y, lobo.x, lobo.y)
        )
        dx = lobo_mais_proximo.x - self.x
        dy = lobo_mais_proximo.y - self.y

        dist = distancia(self.x, self.y, lobo_mais_proximo.x, lobo_mais_proximo.y)
        return [dx / (dist + 1e-5), dy / (dist + 1e-5)]
