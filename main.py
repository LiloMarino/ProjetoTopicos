import pickle

import neat
import pygame

from core import constantes as const
from core.simulador import Simulador

FPS = 60
MAX_TICKS = 1000


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
    while rodando and tick < MAX_TICKS and not simulador.terminou():
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        simulador.executar_tick()
        simulador.draw(tela)

        pygame.display.flip()
        clock.tick(FPS)
        tick += 1

    # Após a simulação, atualiza os fitness dos genomas
    fitness_coelhos, fitness_lobos = simulador.obter_fitness()

    for i, (genoma_id, genoma) in enumerate(genomas_coelhos):
        genoma.fitness = fitness_coelhos[i]

    for i, (genoma_id, genoma) in enumerate(genomas_lobos):
        genoma.fitness = fitness_lobos[i]


def run_evolucao_dupla(config_path_coelho, config_path_lobo):
    config_coelho = carregar_config(config_path_coelho)
    config_lobo = carregar_config(config_path_lobo)

    populacao_coelho = neat.Population(config_coelho)
    populacao_lobo = neat.Population(config_lobo)

    populacao_coelho.add_reporter(neat.StdOutReporter(True))
    populacao_coelho.add_reporter(neat.StatisticsReporter())

    populacao_lobo.add_reporter(neat.StdOutReporter(True))
    populacao_lobo.add_reporter(neat.StatisticsReporter())

    geracoes = 50
    for geracao in range(geracoes):
        print(f"\n====== GERAÇÃO {geracao} ======")

        # Cria listas dos genomas de ambas as populações
        genomas_coelhos = []
        populacao_coelho.run(lambda genomas, config: genomas_coelhos.extend(genomas), 1)

        genomas_lobos = []
        populacao_lobo.run(lambda genomas, config: genomas_lobos.extend(genomas), 1)

        # Roda a simulação com os genomas desta geração
        avaliar_genomas(genomas_coelhos, config_coelho, genomas_lobos, config_lobo)

    # Salva os melhores genomas
    with open("melhor_coelho.pkl", "wb") as f:
        pickle.dump(populacao_coelho.best_genome, f)

    with open("melhor_lobo.pkl", "wb") as f:
        pickle.dump(populacao_lobo.best_genome, f)

    print("Melhores genomas salvos!")


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Simulador Ecológico com Coevolução")
    pygame.display.set_mode(const.TAMANHO_TELA)

    const.init_constantes()

    run_evolucao_dupla(const.NEAT_CONFIG_COELHO, const.NEAT_CONFIG_LOBO)

    pygame.quit()
