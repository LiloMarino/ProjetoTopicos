from entidade import Entidade

from core.ambiente import Ambiente


class Coelho(Entidade):
    VELOCIDADE = 3

    def __init__(self, x: int, y: int, sprite, ambiente: Ambiente):
        super().__init__(x, y, sprite)
        self.ambiente = ambiente
