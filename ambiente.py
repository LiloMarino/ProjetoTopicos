import pygame


class Ambiente:
    def __init__(self, fundo_path, mascara_path):
        self.fundo = pygame.image.load(fundo_path).convert()
        self.mascara_surface = pygame.image.load(mascara_path).convert()
        self.mascara = pygame.mask.from_surface(self.mascara_surface)
        self.width, self.height = self.fundo.get_size()

    def desenhar(self, screen):
        screen.blit(self.fundo, (0, 0))

    def posicao_valida(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.mascara.get_at((int(x), int(y))) == 1
        return False
