import random

import pygame


class Coelho:
    def __init__(self, genome, net, sprite):
        self.genome = genome
        self.net = net
        self.sprite = sprite
        self.x = random.randint(50, 600)
        self.y = random.randint(50, 400)
        self.energia = 100
        self.fitness = 0

    def agir(self, inputs):
        output = self.net.activate(inputs)
        self.x += int(output[0] * 5)
        self.y += int(output[1] * 5)

    def desenhar(self, screen):
        screen.blit(self.sprite, (self.x, self.y))
