import pickle

import neat
import pygame

from core import constantes as const
from core.simulador import Simulador
from dynamic_config import aplicar_config_dinamica_segura, log_genome_config


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
    frame_count = 0
    rodando = True
    while rodando and tick < const.MAX_TICKS and not simulador.terminou():
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        if frame_count % const.TICKS_POR_FRAME == 0:
            simulador.executar_tick()
            tick += 1

        tela.fill((0, 0, 0))
        simulador.draw(tela)
        pygame.display.flip()

        clock.tick(const.FPS)  # FPS de renderização
        frame_count += 1

    # Depois, extrai fitness dos agentes
    fitness_coelhos, fitness_lobos = simulador.obter_fitness()

    for i, (_, genoma) in enumerate(genomas_coelhos):
        genoma.fitness = fitness_coelhos[i]
    for i, (_, genoma) in enumerate(genomas_lobos):
        genoma.fitness = fitness_lobos[i]


def treinar_populacoes(
    pop_coelho: neat.Population, pop_lobo: neat.Population, geracoes=50
):
    pop_coelho.reporters.reporters.clear()
    pop_lobo.reporters.reporters.clear()
    for pop in (pop_coelho, pop_lobo):
        pop.add_reporter(neat.StdOutReporter(True))
        pop.add_reporter(neat.StatisticsReporter())

    try:
        for geracao in range(geracoes):
            print(f"\n====== GERAÇÃO {pop_coelho.generation} ======")

            # Pega os genomas atuais para reprocessar a população
            genomas_coelhos = list(pop_coelho.population.items())
            genomas_lobos = list(pop_lobo.population.items())

            # Avaliação dos genomas
            pop_coelho.reporters.start_generation(pop_coelho.generation)
            pop_lobo.reporters.start_generation(pop_lobo.generation)

            avaliar_genomas(
                genomas_coelhos, pop_coelho.config, genomas_lobos, pop_lobo.config
            )

            # Finaliza geração
            pop_coelho.reporters.end_generation(
                pop_coelho.config, pop_coelho.population, pop_coelho.species
            )
            pop_lobo.reporters.end_generation(
                pop_lobo.config, pop_lobo.population, pop_lobo.species
            )

            # Reproduz as populações
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

            # Especiação
            pop_coelho.species.speciate(
                pop_coelho.config, pop_coelho.population, pop_coelho.generation
            )
            pop_lobo.species.speciate(
                pop_lobo.config, pop_lobo.population, pop_lobo.generation
            )

            # Avança geração
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

        # Extrai melhor genoma histórico
        melhor_genoma_coelho = pop_coelho.best_genome
        melhor_genoma_lobo = pop_lobo.best_genome

        # Se não existir melhor_genome (pode acontecer na 1ª gen), pega o atual com maior fitness
        if melhor_genoma_coelho is None:
            melhor_genoma_coelho = max(
                pop_coelho.population.values(), key=lambda g: g.fitness or 0
            )
        if melhor_genoma_lobo is None:
            melhor_genoma_lobo = max(
                pop_lobo.population.values(), key=lambda g: g.fitness or 0
            )

        with open("melhor_coelho.pkl", "wb") as f:
            pickle.dump(melhor_genoma_coelho, f)
        with open("melhor_lobo.pkl", "wb") as f:
            pickle.dump(melhor_genoma_lobo, f)


def testar_melhores(config_path_coelho, config_path_lobo):
    const.TICKS_POR_FRAME = 10  # Reduz a velocidade para melhor visualização
    config_coelho = carregar_config(config_path_coelho)
    config_lobo = carregar_config(config_path_lobo)

    # Carrega as populações inteiras
    with open("melhor_coelho.pkl", "rb") as f:
        best_coelho = pickle.load(f)
    with open("melhor_lobo.pkl", "rb") as f:
        best_lobo = pickle.load(f)

    num_coelhos = config_coelho.pop_size
    num_lobos = config_lobo.pop_size

    # Cria listas de um único genoma para avaliação
    genomas_coelhos = [(0, best_coelho)]
    genomas_lobos = [(0, best_lobo)]

    rodando = True
    while rodando:
        # Clona os melhores para criar uma nova simulação
        genomas_coelhos = [
            (i, pickle.loads(pickle.dumps(best_coelho))) for i in range(num_coelhos)
        ]
        genomas_lobos = [
            (i, pickle.loads(pickle.dumps(best_lobo))) for i in range(num_lobos)
        ]

        # Avalia e executa a simulação (inclui visualização)
        avaliar_genomas(genomas_coelhos, config_coelho, genomas_lobos, config_lobo)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False


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

        aplicar_config_dinamica_segura(pop_coelho.config, config_coelho)
        aplicar_config_dinamica_segura(pop_lobo.config, config_lobo)
        log_genome_config(pop_coelho.config, "genome_config_coelho_log.txt")
        log_genome_config(pop_lobo.config, "genome_config_lobo_log.txt")
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
