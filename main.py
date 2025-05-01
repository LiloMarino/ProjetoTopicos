import pickle

import neat
import pygame

from core import constantes as const
from core.simulador import Simulador


def carregar_config(caminho):
    return neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        str(caminho),
    )


def avaliar_genomas(genomas_coelhos, config_coelho, genomas_lobos, config_lobo):
    # Cria o simulador com os genomas de ambas as espécies
    simulador = Simulador(genomas_coelhos, genomas_lobos, config_coelho, config_lobo)

    tela = pygame.display.set_mode(const.TAMANHO_TELA)
    clock = pygame.time.Clock()

    tick = 0
    rodando = True
    while rodando and tick < const.MAX_TICKS and not simulador.terminou():
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        simulador.executar_tick()
        tela.fill((0, 0, 0))
        simulador.draw(tela)

        pygame.display.flip()
        clock.tick(const.FPS)
        tick += 1

    # Depois, extrai fitness dos agentes
    fitness_coelhos, fitness_lobos = simulador.obter_fitness()

    for i, (_, genoma) in enumerate(genomas_coelhos):
        genoma.fitness = fitness_coelhos[i]
    for i, (_, genoma) in enumerate(genomas_lobos):
        genoma.fitness = fitness_lobos[i]


def run_evolucao_dupla(config_path_coelho, config_path_lobo):
    config_coelho = carregar_config(config_path_coelho)
    config_lobo = carregar_config(config_path_lobo)

    pop_coelho = neat.Population(config_coelho)
    pop_lobo = neat.Population(config_lobo)

    pop_coelho.add_reporter(neat.StdOutReporter(True))
    pop_coelho.add_reporter(neat.StatisticsReporter())
    pop_lobo.add_reporter(neat.StdOutReporter(True))
    pop_lobo.add_reporter(neat.StatisticsReporter())

    geracoes = 50
    for geracao in range(geracoes):
        print(f"\n====== GERAÇÃO {geracao} ======")

        # Gera listas de (id, genome)
        genomas_coelhos = list(pop_coelho.population.items())
        genomas_lobos = list(pop_lobo.population.items())

        # Reporta início
        pop_coelho.reporters.start_generation(pop_coelho.generation)
        pop_lobo.reporters.start_generation(pop_lobo.generation)

        # Avalia
        avaliar_genomas(genomas_coelhos, config_coelho, genomas_lobos, config_lobo)

        # Reporta fim e reproduz
        pop_coelho.reporters.end_generation(
            config_coelho, pop_coelho.population, pop_coelho.species
        )
        pop_lobo.reporters.end_generation(
            config_lobo, pop_lobo.population, pop_lobo.species
        )

        pop_coelho.population = pop_coelho.reproduction.reproduce(
            config_coelho,
            pop_coelho.species,
            config_coelho.pop_size,
            pop_coelho.generation,
        )
        pop_lobo.population = pop_lobo.reproduction.reproduce(
            config_lobo, pop_lobo.species, config_lobo.pop_size, pop_lobo.generation
        )

        pop_coelho.species.speciate(
            config_coelho, pop_coelho.population, pop_coelho.generation
        )
        pop_lobo.species.speciate(config_lobo, pop_lobo.population, pop_lobo.generation)

        pop_coelho.generation += 1
        pop_lobo.generation += 1

    # Salva melhores
    with open("melhor_coelho.pkl", "wb") as f:
        pickle.dump(pop_coelho.best_genome, f)
    with open("melhor_lobo.pkl", "wb") as f:
        pickle.dump(pop_lobo.best_genome, f)

    print("Melhores genomas salvos!")


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Simulador Ecológico com Coevolução")
    pygame.display.set_mode(const.TAMANHO_TELA)
    const.init_constantes()
    run_evolucao_dupla(const.NEAT_CONFIG_COELHO, const.NEAT_CONFIG_LOBO)
    pygame.quit()
