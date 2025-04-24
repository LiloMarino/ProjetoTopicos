import pygame


class Ambiente:
    def __init__(self, background):
        self.background = background
        self.comida = [(300, 200)]  # posição estática por enquanto

    def desenhar(self, screen):
        screen.blit(self.background, (0, 0))
        for c in self.comida:
            pygame.draw.circle(screen, (0, 255, 0), c, 5)
