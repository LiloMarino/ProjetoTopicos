import os
import sys

import numpy as np
import pygame

# Adiciona o diretório raiz ao sys.path para importar a pasta 'core'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core import constantes as const

# Inicializa o Pygame
pygame.init()

# Inicializa a janela Pygame
screen = pygame.display.set_mode(const.TAMANHO_TELA)
pygame.display.set_caption("Visualização da Máscara de Movimento")

# Carrega a imagem de máscara e converte para RGB
mask_img = pygame.image.load(const.PATH_AMBIENTE_MASK).convert()
mask_img = pygame.transform.scale(mask_img, const.TAMANHO_TELA)
width, height = mask_img.get_size()

# Cria uma nova superfície para a visualização da máscara
debug_surface = pygame.Surface((width, height))


# Função para verificar colisão (simulando como no seu código)
def have_collision(x: float, y: float) -> bool:
    x = int(x)
    y = int(y)
    # Verifica se está dentro dos limites da imagem
    if x < 0 or y < 0 or x >= width or y >= height:
        return True  # Fora dos limites, considera colisão
    # Retorna True se NÃO for "andável" (preto no mask)
    return not mask_img.get_at((x, y))  # A máscara é preto, então True se for proibido


# Pinta a superfície com base na máscara
for y in range(height):
    for x in range(width):
        if have_collision(x, y):
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
