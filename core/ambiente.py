import math
import random
import time

import numpy as np
import pygame
from pygame import Surface

from core import constantes as const


class Ambiente:
    RESPAWN_CENOURA = 10

    def __init__(self, n_cenouras: int = 10):
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

        # Converte imagem de máscara para array numpy de 3 canais (RGB)
        surf_array = pygame.surfarray.array3d(self.img_ambiente_mask)  # shape (w, h, 3)

        # Define como obstáculo todos os pixels pretos (0,0,0)
        self.mask_binaria = np.all(
            surf_array == [0, 0, 0], axis=-1
        ).T  # Transposto para (x, y)

        self.width = self.img_ambiente.get_width()
        self.height = self.img_ambiente.get_height()

        self.cenouras: list[tuple[int, int]] = []  # Lista de cenouras no ambiente
        self.cenouras_em_espera: list[float] = []  # Lista de cenouras para spawnar

        # Inicializa aleatoriamente as cenouras em posições válidas
        for _ in range(n_cenouras):
            self.gerar_cenoura()

    def gerar_cenoura(self):
        w, h = self.img_cenoura.get_size()
        while True:
            # Gera uma posição aleatória onde o CENTRO da cenoura esteja dentro da tela
            x = random.randint(w // 2, self.width - w // 2)
            y = random.randint(h // 2, self.height - h // 2)

            # Verifica se a posição gerada está livre
            if not self.mask_binaria[x, y]:
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

    # @draw_coords_list(pos_attr_name="cenouras", sprite_attr_name="img_cenoura")
    def draw(self, screen: Surface):
        screen.blit(self.img_ambiente, (0, 0))
        w, h = self.img_cenoura.get_size()
        for x, y in self.cenouras:
            screen.blit(self.img_cenoura, (x - w // 2, y - h // 2))

    def have_collision(self, x: float, y: float) -> bool:
        x = int(x)
        y = int(y)
        # Verifica se está dentro dos limites da imagem
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return True
        # Retorna True se for preto no mask
        return self.mask_binaria[x, y]

    def detect_obstacles(
        self, x_centro: float, y_centro: float, w: int, h: int
    ) -> tuple[bool, bool, bool, bool]:
        """
        Retorna uma tupla de 4 booleans (up, down, left, right) indicando
        se há colisão logo acima, abaixo, à esquerda e à direita da hitbox
        centrada em (x_centro, y_centro) com tamanho w x h.
        """
        half_w, half_h = w / 2, h / 2
        x = x_centro - half_w
        y = y_centro - half_h
        pontos = [
            (x + half_w, y),  # Meio superior
            (x, y),  # Canto superior esquerdo
            (x + w, y),  # Canto superior direito
            (x, y + half_h),  # Meio esquerdo
            (x + w, y + half_h),  # Meio direito
            (x, y + h),  # Canto inferior esquerdo
            (x + w, y + h),  # Canto inferior direito
            (x + half_w, y + h),  # Meio inferior
        ]
        up = any(self.have_collision(x, y) for x, y in pontos[:3])
        down = any(self.have_collision(x, y) for x, y in pontos[5:])
        left = any(self.have_collision(x, y) for x, y in pontos[1:6:2])
        right = any(self.have_collision(x, y) for x, y in pontos[2:7:2])
        return up, down, left, right

    def have_collision_hitbox(
        self, x_centro: float, y_centro: float, w: int, h: int
    ) -> bool:
        """
        Verifica colisão nos quatro cantos e nos quatro pontos médios das arestas da hitbox,
        a partir do centro da hitbox:
        - Cantos: (x, y), (x+w, y), (x, y+h), (x+w, y+h)
        - Meios:  (x+w/2, y), (x, y+h/2), (x+w, y+h/2), (x+w/2, y+h)
        Retorna True se QUALQUER ponto estiver colidindo.
        """
        return any(self.detect_obstacles(x_centro, y_centro, w, h))

    def get_local_occupancy_grid(self, x_centro: float, y_centro: float) -> list[int]:
        """
        Retorna 8 valores (0 ou 1) com occupancy grid 3x3 ao redor da hitbox.
        """
        half_w, half_h = const.TAMANHO_SPRITE[0] / 2, const.TAMANHO_SPRITE[1] / 2
        cell_w, cell_h = const.TAMANHO_SPRITE
        xc, yc = int(x_centro), int(y_centro)

        offsets = [
            (-1, -1),
            (0, -1),
            (1, -1),  # cima esquerda, cima, cima direita
            (-1, 0),
            (1, 0),  # esquerda,      , direita
            (-1, 1),
            (0, 1),
            (1, 1),
        ]  # baixo esquerda, baixo, baixo direita

        result = []

        for dx, dy in offsets:
            # Canto da célula
            x0 = xc + dx * cell_w - half_w
            y0 = yc + dy * cell_h - half_h

            # Limites do slice
            x1 = int(x0)
            y1 = int(y0)
            x2 = x1 + cell_w
            y2 = y1 + cell_h

            # Clipe aos limites do mapa
            x1c, x2c = max(0, x1), min(self.width, x2)
            y1c, y2c = max(0, y1), min(self.height, y2)

            # Se a célula está totalmente fora do mapa, considere obstáculo
            if x1c >= x2c or y1c >= y2c:
                result.append(1)
                continue

            # Verifica ocupação na mask_binaria
            occupied = self.mask_binaria[x1c:x2c, y1c:y2c].any()
            result.append(1 if occupied else 0)

        return result
