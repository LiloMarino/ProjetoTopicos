import pygame


class Ambiente:
    def __init__(self, background, mascara):
        self.background = background
        self.mascara = pygame.mask.from_surface(mascara)

    def desenhar(self, screen):
        screen.blit(self.background, (0, 0))

    def posicao_valida(self, x, y):
        """Verifica se a posição (x, y) é andável"""
        try:
            return self.mascara.get_at((int(x), int(y))) == 1
        except IndexError:
            return False  # Fora do mapa
