import math
import random
import time

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

        # Cria a máscara a partir da versão redimensionada
        self.img_ambiente_mask.set_colorkey(
            (255, 255, 255)
        )  # Define a cor branca como transparente
        self.img_ambiente_mask = pygame.mask.from_surface(self.img_ambiente_mask)

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
            if not self.img_ambiente_mask.get_at((x, y)):
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
        return self.img_ambiente_mask.get_at((x, y))

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

    def get_nearest_obstacle_info(
        self, x: float, y: float, max_dist: float = 150, steps: int = 36
    ):
        """
        Retorna a direção normalizada e a distância até o obstáculo mais próximo.
        A varredura é feita em vários ângulos a partir da posição (x, y).
        """
        closest_distance = max_dist
        closest_dx, closest_dy = 0, 0

        for i in range(steps):
            angle = (2 * math.pi / steps) * i
            dx = math.cos(angle)
            dy = math.sin(angle)

            for d in range(1, int(max_dist)):
                tx = int(x + dx * d)
                ty = int(y + dy * d)
                if self.have_collision(tx, ty):
                    if d < closest_distance:
                        closest_distance = d
                        closest_dx = dx
                        closest_dy = dy
                    break

        direction = (closest_dx, closest_dy)
        normalized_distance = closest_distance / max_dist  # [0, 1]
        return direction, normalized_distance
