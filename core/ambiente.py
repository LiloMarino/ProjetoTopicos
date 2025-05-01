import random
import time

from pygame import Surface

from core import constantes as const


class Ambiente:
    RESPAWN_CENOURA = 10

    def __init__(self, n_cenouras: int = 5):
        self.img_ambiente = const.IMG_AMBIENTE
        self.img_ambiente_mask = const.IMG_AMBIENTE_MASK
        self.img_cenoura = const.IMG_CENOURA
        self.width = self.img_ambiente.get_width()
        self.height = self.img_ambiente.get_height()
        self.cenouras: list[tuple[int, int]] = []  # Lista de cenouras no ambiente
        self.cenouras_em_espera: list[float] = []  # Lista de cenouras para spawnar

        # Inicializa aleatoriamente as cenouras em posições válidas
        for _ in range(n_cenouras):
            self.gerar_cenoura()

    def gerar_cenoura(self):
        while True:
            # Gera uma posição aleatoria
            x = random.randint(50, self.width - 50)
            y = random.randint(50, self.height - 50)

            # Verifica se a posição gerada está livre
            if self.img_ambiente_mask.get_at((x, y)):
                self.cenouras.append((x, y))
                break

    def remove_cenoura(self, x: int, y: int):
        if (x, y) in self.cenouras:
            self.cenouras.remove((x, y))
            reaparecimento = time.time() + self.RESPAWN_CENOURA
            self.cenouras_em_espera.append(reaparecimento)

    def get_nearest_cenoura(self, x: float, y: float):
        if not self.cenouras:
            return None
        # Calcula a distância sem a raiz quadrada para melhor desempenho
        return min(self.cenouras, key=lambda pos: (pos[0] - x) ** 2 + (pos[1] - y) ** 2)

    def update(self):
        # Verifica se alguma cenoura está pronta pra reaparecer
        tempo_atual = time.time()
        prontas = [t for t in self.cenouras_em_espera if t <= tempo_atual]
        for _ in prontas:
            self.gerar_cenoura()
            self.cenouras_em_espera.remove(_)

    def draw(self, screen: Surface):
        screen.blit(self.img_ambiente, (0, 0))
        for x, y in self.cenouras:
            screen.blit(self.img_cenoura, (x, y))

    def have_collision(self, x: float, y: float) -> bool:
        x = int(x)
        y = int(y)
        # Retorna True se NÃO for "andável" (preto no mask)
        return not self.img_ambiente_mask.get_at((x, y))
