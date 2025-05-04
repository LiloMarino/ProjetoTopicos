import random
from typing import List, Set

import neat.nn
from pygame import Surface

from core.ambiente import Ambiente
from core.coelho import Coelho
from core.lobo import Lobo


class Simulador:
    def __init__(self, genomas_coelhos, genomas_lobos, config_coelho, config_lobo):
        self.ambiente = Ambiente()
        self.coelhos: List[Coelho] = []
        self.lobos: List[Lobo] = []

        # Instancia e inicializa coelhos
        for gid, genome in genomas_coelhos:
            net = neat.nn.FeedForwardNetwork.create(genome, config_coelho)
            x, y = self._spawn_point()
            self.coelhos.append(Coelho(x, y, net, self))
            genome.fitness = 0.0

        # Instancia e inicializa lobos
        for gid, genome in genomas_lobos:
            net = neat.nn.FeedForwardNetwork.create(genome, config_lobo)
            x, y = self._spawn_point()
            self.lobos.append(Lobo(x, y, net, self))
            genome.fitness = 0.0

        self.coelhos_vivos: Set[Coelho] = set(self.coelhos)
        self.lobos_vivos: Set[Lobo] = set(self.lobos)
        self.tempo_total = 0

    def _spawn_point(self):
        # Gera uma posição aleatória válida no ambiente.
        while True:
            x = random.randint(50, self.ambiente.width - 50)
            y = random.randint(50, self.ambiente.height - 50)
            if not self.ambiente.have_collision(x, y):
                return x, y

    def executar_tick(self):
        # Atualiza todos os elementos do simulador por um tick.
        self.tempo_total += 1
        self.ambiente.update()
        for c in self.coelhos:
            c.update(self.ambiente, self.lobos_vivos)
        for l in self.lobos:
            l.update(self.ambiente, self.coelhos_vivos)

    def draw(self, screen: Surface):
        # Desenha o estado atual do simulador.
        self.ambiente.draw(screen)
        for c in self.coelhos:
            c.draw(screen)
        for l in self.lobos:
            l.draw(screen)

    def terminou(self):
        # Termina se uma das populações acabar
        return not any(c.vivo for c in self.coelhos) or not any(
            l.vivo for l in self.lobos
        )

    def obter_fitness(self):
        return ([c.fitness for c in self.coelhos], [l.fitness for l in self.lobos])
