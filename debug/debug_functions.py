import functools

import pygame

from core import constantes as const


def draw_coords(func):
    """Decorator para desenhar as coordenadas do objeto com .x e .y"""

    @functools.wraps(func)
    def wrapper(self, screen: pygame.Surface, *args, **kwargs):
        result = func(self, screen, *args, **kwargs)

        if hasattr(self, "x") and hasattr(self, "y"):
            text = const.FONT.render(
                f"({int(self.x)}, {int(self.y)})", True, (255, 255, 255)
            )
            screen.blit(
                text,
                (
                    self.x + const.TAMANHO_SPRITE[0] / 2,
                    self.y - const.TAMANHO_SPRITE[1] / 2,
                ),
            )
        return result

    return wrapper


def draw_coords_list(pos_attr_name="cenouras", sprite_attr_name="img_cenoura"):
    """
    Decorator para desenhar as coordenadas de uma lista de posições.

    :param pos_attr_name: nome do atributo da lista (ex: "cenouras")
    :param sprite_attr_name: nome do sprite para ajuste de offset
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, screen: pygame.Surface, *args, **kwargs):
            result = func(self, screen, *args, **kwargs)

            coords = getattr(self, pos_attr_name, [])
            sprite = getattr(self, sprite_attr_name, None)
            if sprite is None:
                return result

            w, h = sprite.get_size()
            for x, y in coords:
                text = const.FONT.render(f"({x}, {y})", True, (255, 255, 255))
                screen.blit(
                    text,
                    (
                        x + const.TAMANHO_SPRITE[0] / 2,
                        y - const.TAMANHO_SPRITE[1] / 2,
                    ),
                )
            return result

        return wrapper

    return decorator
