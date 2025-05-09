import os
import sys

import numpy as np
import pygame

# Adiciona o diretório raiz ao sys.path para importar a pasta 'core'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core import constantes as const
from core.ambiente import Ambiente

# Inicializa o Pygame
pygame.init()
pygame.display.set_caption("Simulador Ecológico com Coevolução")
screen = pygame.display.set_mode(const.TAMANHO_TELA)
const.init_constantes()

ambient = Ambiente()

# Cria uma nova superfície para a visualização da máscara
debug_surface = pygame.Surface(const.TAMANHO_TELA)

# Pinta a superfície com base na máscara
for y in range(const.TAMANHO_TELA[1]):
    for x in range(const.TAMANHO_TELA[0]):
        if ambient.have_collision(x, y):
            debug_surface.set_at((x, y), (255, 0, 0))  # Vermelho = proibido
        else:
            debug_surface.set_at((x, y), (0, 255, 0))  # Verde = pode andar

# Loop de exibição
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))  # Limpa a tela com fundo preto
    screen.blit(debug_surface, (0, 0))  # Desenha a superfície da máscara
    pygame.display.flip()

pygame.quit()
