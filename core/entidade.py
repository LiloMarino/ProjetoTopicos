import pygame
from pygame import Surface


class Entidade:
    def __init__(self, x: float, y: float, sprite: Surface):
        self.x = x
        self.y = y
        self.sprite = sprite

    def move(self, dx: float, dy: float):
        self.x += dx
        self.y += dy

    def get_pos(self):
        return self.x, self.y

    # @draw_coords
    def draw(self, screen: Surface):
        w, h = self.sprite.get_size()
        screen.blit(self.sprite, (int(self.x - w / 2), int(self.y - h / 2)))

    def aplicar_tom_vermelho(self):
        # Aplica efeito de tom vermelho para indicar morte
        vermelho = pygame.Surface(self.sprite.get_size()).convert_alpha()
        vermelho.fill((255, 0, 0, 100))  # Vermelho semi-transparente
        sprite_avermelhado = self.sprite.copy()
        sprite_avermelhado.blit(vermelho, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        self.sprite = sprite_avermelhado
