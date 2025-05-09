import math

import neat

from core import constantes as const
from core.ambiente import Ambiente
from core.entidade import Entidade


class Lobo(Entidade):
    VELOCIDADE = 3.5

    def __init__(
        self, x: float, y: float, cerebro: neat.nn.FeedForwardNetwork, simulador
    ):
        super().__init__(x, y, const.IMG_LOBO)
        self.cerebro = cerebro
        self.simulador = simulador
        self.vivo = True
        self.fitness = 0
        self.tempo_vivo = 0
        self.coelhos_comidos = 0
        self.distancia_coelho_anterior = None
        self.aproximou_do_coelho = 0
        self.distanciou_do_coelho = 0
        self.colisao_obstaculo = 0

    def get_inputs(self, ambiente: Ambiente, coelhos_vivos: set):
        cx, cy = self.get_pos()

        # Coelho mais próximo (vivo)
        if coelhos_vivos:
            coelho = min(coelhos_vivos, key=lambda c: (c.x - cx) ** 2 + (c.y - cy) ** 2)
            dx_coelho = coelho.x - cx
            dy_coelho = coelho.y - cy
            dist_coelho = math.hypot(dx_coelho, dy_coelho)
        else:
            dx_coelho = dy_coelho = dist_coelho = 0

        # Direção do coelho mais próximo
        direction_coelho = (
            (dx_coelho / dist_coelho, dy_coelho / dist_coelho)
            if dist_coelho != 0
            else (0, 0)
        )

        # Normaliza a distância com base no tamanho do ambiente
        dist_coelho_norm = dist_coelho / ambiente.width

        # Obstáculos
        w, h = self.sprite.get_size()
        up, down, left, right = ambiente.detect_obstacles(cx, cy, w, h)
        obstaculos = [int(up), int(down), int(left), int(right)]

        # Grid 3x3 de obstáculos ao redor do agente (8 inputs)
        grid_obstaculos = ambiente.get_local_occupancy_grid(cx, cy)

        return [
            dist_coelho_norm,
            *direction_coelho,
            *obstaculos,
            *grid_obstaculos,
        ], dist_coelho

    def calcular_fitness(self):
        self.fitness = 0
        self.fitness -= self.tempo_vivo * 1  # -1 por tempo vivo
        self.fitness += 100 * self.coelhos_comidos  # +100 por coelho comido
        self.fitness -= 2 * self.colisao_obstaculo  # -2 por colisão com obstáculo
        self.fitness -= self.distanciou_do_coelho  # +1 por cada vez que se afastou
        if not self.vivo:
            self.fitness -= 100  # -100 por morrer

    def update(self, ambiente: Ambiente, coelhos_vivos: set):
        if not self.vivo:
            return

        self.tempo_vivo += 1

        inputs, dist_coelho_atual = self.get_inputs(ambiente, coelhos_vivos)
        outputs = self.cerebro.activate(inputs)  # [cima, baixo, direita, esquerda]

        dx = (outputs[2] - outputs[3]) * self.VELOCIDADE
        dy = (outputs[1] - outputs[0]) * self.VELOCIDADE

        # Tenta se mover
        nova_x, nova_y = self.x + dx, self.y + dy
        w, h = self.sprite.get_size()
        if not ambiente.have_collision_hitbox(nova_x, nova_y, w, h):
            self.move(dx, dy)

        # Verifica se pegou coelho
        coelhos_mortos = []
        for coelho in coelhos_vivos:
            if math.hypot(self.x - coelho.x, self.y - coelho.y) < const.ACTION_RANGE:
                coelhos_mortos.append(coelho)
                self.coelhos_comidos += 1
        for coelho in coelhos_mortos:
            coelho.morrer()

        # Verifica se se aproximou do coelho
        if self.distancia_coelho_anterior is not None:
            if dist_coelho_atual < self.distancia_coelho_anterior:
                self.aproximou_do_coelho += 1
            else:
                self.distanciou_do_coelho += 1
        self.distancia_coelho_anterior = dist_coelho_atual

        # Verifica se colidiu com obstáculo
        w, h = self.sprite.get_size()
        if ambiente.have_collision_hitbox(self.x, self.y, w, h):
            self.colisao_obstaculo += 1

        # Verifica se não morreu de fome
        # 20% do tempo total + 10% do tempo total a cada coelho comido
        if (
            self.tempo_vivo
            > const.MAX_TICKS * 0.2 + self.coelhos_comidos * const.MAX_TICKS * 0.10
        ):
            self.morrer()

        # Recalcula o fitness com base nas métricas acumuladas
        self.calcular_fitness()

    def morrer(self):
        self.vivo = False
        self.simulador.lobos_vivos.discard(self)
        self.aplicar_tom_vermelho()
