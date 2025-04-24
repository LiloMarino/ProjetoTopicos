import os

import neat
import pygame

from agentes import Coelho
from ambiente import Ambiente

WIDTH, HEIGHT = 800, 600


def simular_partida(coelho, screen, ambiente, clock):
    tempo_max = 300
    for _ in range(tempo_max):
        pygame.event.pump()
        ambiente.desenhar(screen)

        # Mock de entrada do agente (colocar lógica real depois)
        inputs = [1, 0, 0, 1, 0]
        coelho.agir(inputs)
        coelho.desenhar(screen)

        pygame.display.flip()
        clock.tick(30)

        coelho.fitness += 0.1  # Exemplo: sobreviveu = ganha fitness


def avaliar_genomas(genomas, config):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simulador de Ecossistema")
    clock = pygame.time.Clock()

    assets_path = os.path.join(os.path.dirname(__file__), "assets")
    fundo = pygame.image.load(os.path.join(assets_path, "ambiente.png"))
    sprite_coelho = pygame.image.load(os.path.join(assets_path, "cueio.png"))

    for _, genome in genomas:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        coelho = Coelho(genome, net, sprite_coelho)
        ambiente = Ambiente(fundo)
        simular_partida(coelho, screen, ambiente, clock)
        genome.fitness = coelho.fitness

    pygame.quit()
