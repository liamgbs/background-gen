from random import random, randint
from math import sin, cos, radians
from helpers import randomColour


class FractalTree():
    def __init__(self, imgx, imgy, imgdraw):
        self.imgx = imgx
        self.imgy = imgy
        self.imgdraw = imgdraw
        self.branch_mutator = None

    @staticmethod
    def colour_darken(col, by=20):
        return tuple(map(lambda x : (x - by), col))

    @staticmethod
    def colour_lighten(col, by=20):
        return tuple(map(lambda x : (x + by), col))

    def draw(self, x, y, angle, branches, branch_width, colour, bright=False):
        self.branch_mutator = self.colour_darken if bright else self.colour_lighten
        self._draw(x, y, angle, branches, branch_width, colour)

    def _draw(self, x, y, angle, branches, branch_width, colour):
        if branches == 0:
            return

        x2 = x + cos(radians(angle)) * branches * (self.imgx / 100)
        y2 = y + sin(radians(angle)) * branches * (self.imgx / 100)

        self.imgdraw.line((x, y, x2, y2), width=branch_width, fill=colour)

        new_colour = self.colour_darken(colour)

        for i in range(randint(2, 3)):
            direction = -1 if random() < 0.5 else 1
            self._draw(x2, y2, angle + (randint(15, 40) * direction), branches - 1, branch_width - 2, self.branch_mutator(colour))
