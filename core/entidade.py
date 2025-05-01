from abc import ABC, abstractmethod

from pygame import Surface

from core.ambiente import Ambiente


class Entidade(ABC):
    def __init__(self, x: float, y: float, sprite: Surface):
        self.x = x
        self.y = y
        self.sprite = sprite

    def move(self, dx: float, dy: float):
        self.x += dx
        self.y += dy

    def get_pos(self):
        return self.x, self.y

    @abstractmethod
    def update(self, ambiente: Ambiente):
        # Aqui deve ser implementado o que a entidade vai fazer a cada frame
        pass

    def draw(self, screen: Surface):
        screen.blit(self.sprite, (int(self.x), int(self.y)))
