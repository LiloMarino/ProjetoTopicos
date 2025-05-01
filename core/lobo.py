from core.ambiente import Ambiente
from core.entidade import Entidade


class Lobo(Entidade):
    VELOCIDADE = 3.5

    def __init__(self, x: int, y: int, sprite, ambiente: Ambiente):
        super().__init__(x, y, sprite)
        self.ambiente = ambiente
