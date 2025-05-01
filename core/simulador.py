import random
from typing import List

import pygame
from pygame import Surface

from core.ambiente import Ambiente
from core.coelho import Coelho
from core.lobo import Lobo


class Simulador:
    def __init__(self, genomas_coelhos, genomas_lobos, config_coelho, config_lobo):
        self.ambiente = Ambiente()
        self.coelhos: List[Coelho] = []
        self.lobos: List[Lobo] = []

        # Cria coelhos
        for g in genomas_coelhos:
            cerebro = config_coelho.genome_type.create(g.key)
            cerebro.configure_new(config_coelho)
            net = config_coelho.genome_type.create_net(g, config_coelho)
            coelho = Coelho(*self._spawn_point(), net)
            self.coelhos.append(coelho)
            g.fitness = 0  # Inicializa o fitness no genoma

        # Cria lobos
        for g in genomas_lobos:
            cerebro = config_lobo.genome_type.create(g.key)
            cerebro.configure_new(config_lobo)
            net = config_lobo.genome_type.create_net(g, config_lobo)
            lobo = Lobo(*self._spawn_point(), net)
            self.lobos.append(lobo)
            g.fitness = 0  # Inicializa o fitness no genoma

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

        for coelho in self.coelhos:
            coelho.update(self.ambiente, self.lobos)

        for lobo in self.lobos:
            lobo.update(self.ambiente, self.coelhos)

    def draw(self, screen: Surface):
        # Desenha o estado atual do simulador.
        self.ambiente.draw(screen)

        for coelho in self.coelhos:
            coelho.draw(screen)

        for lobo in self.lobos:
            lobo.draw(screen)

    def terminou(self):
        # Retorna True se todos os coelhos e lobos estiverem mortos.
        return not any(c.vivo for c in self.coelhos) or not any(
            l.vivo for l in self.lobos
        )

    def obter_fitness(self):
        # Retorna os valores de fitness dos agentes.
        fitness_coelhos = [c.fitness for c in self.coelhos]
        fitness_lobos = [l.fitness for l in self.lobos]
        return fitness_coelhos, fitness_lobos
