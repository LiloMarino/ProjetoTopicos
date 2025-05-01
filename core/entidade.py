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

    def draw(self, screen: Surface):
        screen.blit(self.sprite, (int(self.x), int(self.y)))
