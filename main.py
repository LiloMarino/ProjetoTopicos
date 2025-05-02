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


def treinar_populacoes(
    pop_coelho: neat.Population, pop_lobo: neat.Population, geracoes=50
):
    for pop in (pop_coelho, pop_lobo):
        pop.add_reporter(neat.StdOutReporter(True))
        pop.add_reporter(neat.StatisticsReporter())

    try:
        for geracao in range(geracoes):
            print(f"\n====== GERAÇÃO {geracao} ======")

            genomas_coelhos = list(pop_coelho.population.items())
            genomas_lobos = list(pop_lobo.population.items())

            pop_coelho.reporters.start_generation(pop_coelho.generation)
            pop_lobo.reporters.start_generation(pop_lobo.generation)

            avaliar_genomas(
                genomas_coelhos, pop_coelho.config, genomas_lobos, pop_lobo.config
            )

            pop_coelho.reporters.end_generation(
                pop_coelho.config, pop_coelho.population, pop_coelho.species
            )
            pop_lobo.reporters.end_generation(
                pop_lobo.config, pop_lobo.population, pop_lobo.species
            )

            pop_coelho.population = pop_coelho.reproduction.reproduce(
                pop_coelho.config,
                pop_coelho.species,
                pop_coelho.config.pop_size,
                pop_coelho.generation,
            )
            pop_lobo.population = pop_lobo.reproduction.reproduce(
                pop_lobo.config,
                pop_lobo.species,
                pop_lobo.config.pop_size,
                pop_lobo.generation,
            )

            pop_coelho.species.speciate(
                pop_coelho.config, pop_coelho.population, pop_coelho.generation
            )
            pop_lobo.species.speciate(
                pop_lobo.config, pop_lobo.population, pop_lobo.generation
            )

            pop_coelho.generation += 1
            pop_lobo.generation += 1

    except KeyboardInterrupt:
        print("\nInterrupção detectada! Salvando população…")
    finally:
        with open("pop_coelho.pkl", "wb") as f:
            pickle.dump(pop_coelho, f)
        with open("pop_lobo.pkl", "wb") as f:
            pickle.dump(pop_lobo, f)
        print("Populações salvas!")


def testar_melhores(config_path_coelho, config_path_lobo):
    config_coelho = carregar_config(config_path_coelho)
    config_lobo = carregar_config(config_path_lobo)

    # Carrega os melhores genomas
    with open("pop_coelho.pkl", "rb") as f:
        pop_coelho = pickle.load(f)
    with open("pop_lobo.pkl", "rb") as f:
        pop_lobo = pickle.load(f)

    # Cria listas com um único genoma
    genomas_coelhos = [(0, pop_coelho.best_genome)]
    genomas_lobos = [(0, pop_lobo.best_genome)]

    # Roda a simulação normal (sem NEAT)
    avaliar_genomas(genomas_coelhos, config_coelho, genomas_lobos, config_lobo)


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Simulador Ecológico com Coevolução")
    pygame.display.set_mode(const.TAMANHO_TELA)
    const.init_constantes()

    prompt = (
        "[c]\tContinuar Treinando\n"
        "[n]\tTreinar do Zero\n"
        "[x]\tTestar Melhor Salvo\n"
        "Escolha o modo [default: c]: "
    )
    modo = input(prompt).strip().lower() or "c"

    config_coelho = carregar_config(const.NEAT_CONFIG_COELHO)
    config_lobo = carregar_config(const.NEAT_CONFIG_LOBO)

    if modo == "c":
        try:
            with open("pop_coelho.pkl", "rb") as f:
                pop_coelho = pickle.load(f)
            with open("pop_lobo.pkl", "rb") as f:
                pop_lobo = pickle.load(f)
            print("Populações carregadas, continuando evolução…")
        except FileNotFoundError:
            print("Nenhuma população salva. Criando do zero…")
            pop_coelho = neat.Population(config_coelho)
            pop_lobo = neat.Population(config_lobo)

        treinar_populacoes(pop_coelho, pop_lobo)

    elif modo == "n":
        pop_coelho = neat.Population(config_coelho)
        pop_lobo = neat.Population(config_lobo)
        treinar_populacoes(pop_coelho, pop_lobo)

    elif modo == "x":
        testar_melhores(const.NEAT_CONFIG_COELHO, const.NEAT_CONFIG_LOBO)

    else:
        print("Modo inválido. Use Enter, 'c', 'n' ou 'x'.")

    pygame.quit()
