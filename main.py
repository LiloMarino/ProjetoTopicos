import os
import random

import neat
import pygame
from coelho import Coelho
from lobo import Lobo

from core.ambiente import Ambiente
from core.simulador import Simulador

ASSETS = "assets"


def carregar_imgs():
    coelho_img = pygame.image.load(os.path.join(ASSETS, "cueio.png")).convert_alpha()
    lobo_img = pygame.image.load(os.path.join(ASSETS, "lobo.png")).convert_alpha()
    return coelho_img, lobo_img


def eval_genomes(genomes_coelho, config_coelho, genomes_lobo, config_lobo, ambiente):
    nets_coelho = []
    coelhos = []
    for genome_id, genome in genomes_coelho:
        net = neat.nn.FeedForwardNetwork.create(genome, config_coelho)
        nets_coelho.append(net)
        x = random.randint(50, ambiente.width - 50)
        y = random.randint(50, ambiente.height - 50)
        coelho = Coelho(x, y, coelho_img, ambiente)
        coelhos.append(coelho)
        genome.fitness = 0

    nets_lobo = []
    lobos = []
    for genome_id, genome in genomes_lobo:
        net = neat.nn.FeedForwardNetwork.create(genome, config_lobo)
        nets_lobo.append(net)
        x = random.randint(50, ambiente.width - 50)
        y = random.randint(50, ambiente.height - 50)
        lobo = Lobo(x, y, lobo_img, ambiente)
        lobos.append(lobo)
        genome.fitness = 0

    simulador = Simulador(ambiente, coelhos, lobos)
    clock = pygame.time.Clock()

    run = True
    while run and any(coelho.vivo for coelho in coelhos):
        clock.tick(60)
        simulador.step(nets_coelho, nets_lobo)

        for i, coelho in enumerate(coelhos):
            if coelho.vivo:
                genomes_coelho[i][1].fitness += 0.1  # viver é bom

        for i, lobo in enumerate(lobos):
            genomes_lobo[i][1].fitness += lobo.fitness  # comer é bom

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                exit()

        screen.fill((255, 255, 255))
        simulador.draw(screen)
        pygame.display.update()


def run(config_coelho_path, config_lobo_path):
    pygame.init()
    ambiente = Ambiente(
        os.path.join(ASSETS, "ambiente.png"), os.path.join(ASSETS, "mask_ambiente.png")
    )
    global screen
    screen = pygame.display.set_mode((ambiente.width, ambiente.height))

    global coelho_img, lobo_img
    coelho_img, lobo_img = carregar_imgs()

    config_coelho = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_coelho_path,
    )

    config_lobo = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_lobo_path,
    )

    pop_coelho = neat.Population(config_coelho)
    pop_lobo = neat.Population(config_lobo)

    # Loop manual: rodamos gerações juntos
    for g in range(50):
        print(f"==== Geração {g} ====")
        genomes_coelho = []
        pop_coelho.population.items()
        for genome_id, genome in pop_coelho.population.items():
            genomes_coelho.append((genome_id, genome))

        genomes_lobo = []
        pop_lobo.population.items()
        for genome_id, genome in pop_lobo.population.items():
            genomes_lobo.append((genome_id, genome))

        eval_genomes(genomes_coelho, config_coelho, genomes_lobo, config_lobo, ambiente)

        pop_coelho.reporters.end_generation(
            config_coelho, pop_coelho.population, pop_coelho.species
        )
        pop_lobo.reporters.end_generation(
            config_lobo, pop_lobo.population, pop_lobo.species
        )


if __name__ == "__main__":
    run("neat-config-coelho.txt", "neat-config-lobo.txt")
