import random
import time

import pygame
from pygame import Surface

from core import constantes as const


class Ambiente:
    RESPAWN_CENOURA = 10

    def __init__(self, n_cenouras: int = 5):
        self.img_ambiente = pygame.image.load(const.PATH_AMBIENTE).convert()
        self.img_ambiente_mask = pygame.image.load(const.PATH_AMBIENTE_MASK).convert()
        self.img_cenoura = const.IMG_CENOURA

        # Redimensiona as imagens do ambiente para o tamanho da tela
        self.img_ambiente = pygame.transform.scale(
            self.img_ambiente, const.TAMANHO_TELA
        )
        self.img_ambiente_mask = pygame.transform.scale(
            self.img_ambiente_mask, const.TAMANHO_TELA
        )

        # Cria a máscara a partir da versão redimensionada
        self.img_ambiente_mask = pygame.mask.from_surface(self.img_ambiente_mask)

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
        # Verifica se está dentro dos limites da imagem
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            # Considera que houve colisão se for fora dos limites
            return True
        # Retorna True se NÃO for "andável" (preto no mask)
        return not self.img_ambiente_mask.get_at((x, y))

    def have_collision_hitbox(self, x: float, y: float, w: int, h: int) -> bool:
        """
        Verifica colisão nos quatro cantos da hitbox:
        (x, y), (x+w, y), (x, y+h), (x+w, y+h)
        Retorna True se QUALQUER ponto estiver colidindo.
        """
        cantos = [
            (x, y),
            (x + w, y),
            (x, y + h),
            (x + w, y + h),
        ]
        for px, py in cantos:
            if self.have_collision(px, py):
                return True
        return False
