import math

from core import constantes as const
from core.ambiente import Ambiente
from core.coelho import Coelho
from core.entidade import Entidade


class Lobo(Entidade):
    VELOCIDADE = 3.5

    def __init__(self, x: float, y: float, cerebro):
        super().__init__(x, y, const.IMG_LOBO)
        self.cerebro = cerebro
        self.vivo = True
        self.fitness = 0
        self.tempo_vivo = 0
        self.coelhos_comidos = 0
        self.distancia_coelho_anterior = None
        self.aproximou_do_coelho = 0

    def get_inputs(self, ambiente: Ambiente, coelhos: list[Coelho]):
        cx, cy = self.get_pos()

        # Coelho mais próximo (vivo)
        coelhos_vivos = [c for c in coelhos if c.vivo]
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
        obstaculos = [
            ambiente.have_collision(cx, cy - 1),  # Norte
            ambiente.have_collision(cx, cy + 1),  # Sul
            ambiente.have_collision(cx + 1, cy),  # Leste
            ambiente.have_collision(cx - 1, cy),  # Oeste
        ]

        return [
            dist_coelho_norm,
            *direction_coelho,
            *map(int, obstaculos),
        ], dist_coelho

    def calcular_fitness(self):
        self.fitness = 0
        self.fitness -= self.tempo_vivo  # -1 por tempo vivo
        self.fitness += 5 * self.coelhos_comidos  # +5 por coelho comido
        self.fitness += self.aproximou_do_coelho  # +1 por cada aproximação de coelho
        if not self.vivo:
            self.fitness -= 10  # -10 por morrer

    def update(self, ambiente: Ambiente, coelhos: list[Coelho]):
        if not self.vivo:
            return

        self.tempo_vivo += 1

        inputs, dist_coelho_atual = self.get_inputs(ambiente, coelhos)
        outputs = self.cerebro.activate(inputs)  # [cima, baixo, direita, esquerda]

        dx = (outputs[2] - outputs[3]) * self.VELOCIDADE
        dy = (outputs[1] - outputs[0]) * self.VELOCIDADE

        # Tenta se mover
        nova_x, nova_y = self.x + dx, self.y + dy
        if not ambiente.have_collision(nova_x, nova_y):
            self.move(dx, dy)

        # Verifica se pegou coelho
        for coelho in coelhos:
            if coelho.vivo and math.hypot(self.x - coelho.x, self.y - coelho.y) < 20:
                coelho.morrer()
                self.coelhos_comidos += 1

        # Verifica se se aproximou do coelho
        if self.distancia_coelho_anterior is not None:
            if dist_coelho_atual < self.distancia_coelho_anterior:
                self.aproximou_do_coelho += 1
        self.distancia_coelho_anterior = dist_coelho_atual

        # Recalcula o fitness com base nas métricas acumuladas
        self.calcular_fitness()

    def morrer(self):
        self.vivo = False
