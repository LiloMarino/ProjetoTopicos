import pygame

from utils import distancia


class Simulador:
    def __init__(self, ambiente, coelhos, lobos):
        self.ambiente = ambiente
        self.coelhos = coelhos
        self.lobos = lobos

    def step(self, nets_coelhos, nets_lobos):
        # Atualizar Coelhos
        for i, coelho in enumerate(self.coelhos):
            if coelho.vivo:
                inputs = coelho.calcular_inputs(self.lobos)
                output = nets_coelhos[i].activate(inputs)
                coelho.mover(output)

        # Atualizar Lobos
        for i, lobo in enumerate(self.lobos):
            if lobo.vivo:
                inputs = lobo.calcular_inputs(self.coelhos)
                output = nets_lobos[i].activate(inputs)
                lobo.mover(output)

        # Verificar capturas
        for lobo in self.lobos:
            for coelho in self.coelhos:
                if coelho.vivo and distancia(lobo.x, lobo.y, coelho.x, coelho.y) < 20:
                    coelho.vivo = False
                    lobo.fitness += 50

    def desenhar(self, screen):
        self.ambiente.desenhar(screen)
        for coelho in self.coelhos:
            if coelho.vivo:
                coelho.desenhar(screen)
        for lobo in self.lobos:
            if lobo.vivo:
                lobo.desenhar(screen)
