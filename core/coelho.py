import math

from core import constantes as const
from core.ambiente import Ambiente
from core.entidade import Entidade


class Coelho(Entidade):
    VELOCIDADE = 3

    def __init__(self, x: float, y: float, cerebro):
        super().__init__(x, y, const.IMG_COELHO)
        self.cerebro = cerebro
        self.vivo = True
        self.fitness = 0
        self.tempo_vivo = 0
        self.cenouras_comidas = 0
        self.distancia_lobo_anterior = None
        self.distanciou_do_lobo = 0

    def get_inputs(self, ambiente: Ambiente, lobos: list):
        cx, cy = self.get_pos()

        # Cenoura mais próxima
        cenoura = ambiente.get_nearest_cenoura(cx, cy)
        if cenoura:
            dx_cenoura = cenoura[0] - cx
            dy_cenoura = cenoura[1] - cy
            dist_cenoura = math.hypot(dx_cenoura, dy_cenoura)
        else:
            dx_cenoura = dy_cenoura = dist_cenoura = 0

        # Direção da cenoura mais próxima
        direction_cenoura = (
            (dx_cenoura / dist_cenoura, dy_cenoura / dist_cenoura)
            if dist_cenoura != 0
            else (0, 0)
        )

        # Lobo mais próximo (vivo)
        lobos_vivos = [l for l in lobos if l.vivo]
        if lobos_vivos:
            lobo = min(lobos_vivos, key=lambda l: (l.x - cx) ** 2 + (l.y - cy) ** 2)
            dx_lobo = lobo.x - cx
            dy_lobo = lobo.y - cy
            dist_lobo = math.hypot(dx_lobo, dy_lobo)
        else:
            dx_lobo = dy_lobo = dist_lobo = 0

        # Direção do lobo mais próximo
        direction_lobo = (
            (dx_lobo / dist_lobo, dy_lobo / dist_lobo) if dist_lobo != 0 else (0, 0)
        )

        # Normaliza as distâncias com base no tamanho do ambiente
        dist_cenoura_norm = dist_cenoura / ambiente.width
        dist_lobo_norm = dist_lobo / ambiente.width

        # Obstáculos
        obstaculos = [
            ambiente.have_collision(cx, cy - 1),
            ambiente.have_collision(cx, cy + 1),
            ambiente.have_collision(cx + 1, cy),
            ambiente.have_collision(cx - 1, cy),
        ]

        return [
            dist_cenoura_norm,
            *direction_cenoura,
            dist_lobo_norm,
            *direction_lobo,
            *map(int, obstaculos),
        ], dist_lobo

    def calcular_fitness(self):
        self.fitness = 0
        self.fitness += self.tempo_vivo  # +1 por tempo vivo
        self.fitness += 5 * self.cenouras_comidas  # +5 por cenoura
        self.fitness += self.distanciou_do_lobo  # +1 por cada vez que se afastou
        if not self.vivo:
            self.fitness -= 10  # -10 por morrer

    def update(self, ambiente: Ambiente, lobos: list):
        if not self.vivo:
            return

        self.tempo_vivo += 1

        inputs, dist_lobo_atual = self.get_inputs(ambiente, lobos)
        outputs = self.cerebro.activate(inputs)  # [cima, baixo, direita, esquerda]

        dx = (outputs[2] - outputs[3]) * self.VELOCIDADE
        dy = (outputs[1] - outputs[0]) * self.VELOCIDADE

        # Tenta se mover
        nova_x, nova_y = self.x + dx, self.y + dy
        if not ambiente.have_collision(nova_x, nova_y):
            self.move(dx, dy)

        # Verifica se comeu cenoura
        for cenoura in ambiente.cenouras:
            if math.hypot(self.x - cenoura[0], self.y - cenoura[1]) < 20:
                ambiente.remove_cenoura(*cenoura)
                self.cenouras_comidas += 1

        # Distância ao lobo: se aumentou desde o último tick, considera como "fuga bem sucedida"
        if self.distancia_lobo_anterior is not None:
            if dist_lobo_atual > self.distancia_lobo_anterior:
                self.distanciou_do_lobo += 1
        self.distancia_lobo_anterior = dist_lobo_atual

        # Após todas as atualizações de estado, recalcula o fitness
        self.calcular_fitness()

    def morrer(self):
        self.vivo = False
