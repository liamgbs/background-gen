from random import choice
from math import sqrt

class Colours:
    def __init__(self, ba):
        self.cols = [
            # purples
            [(85, 18, 127, ba), (199, 112, 255, ba), (169, 35, 255, ba), (100, 56, 127, ba), (135, 28, 204, ba)],
            # greens
            [(31, 181, 255, ba), (28, 218, 232, ba), (44, 255, 211, ba), (28, 232, 132, ba), (32, 255, 81, ba)],
            # orange, brown, pink, green, green
            [(204, 69, 42, ba), (153, 98, 87, ba), (255, 44, 136, ba), (152, 255, 107, ba), (138, 204, 15, ba)],
            # green, blue, lime, orange, tan
            [(77, 178, 3, ba), (55, 84, 255, ba), (125, 255, 29, ba), (204, 55, 3, ba), (178, 136, 109, ba)],
            # blue, green, yellow, salmon, violet
            [(118, 147, 255, ba), (107, 232, 139, ba), (255, 232, 131, ba), (232, 169, 163, ba), (143, 118, 255, ba)],
            # pinks
            [(191, 43, 122, ba), (127, 28, 81, ba), (255, 57, 162, ba), (64, 14, 41, ba), (229, 51, 146, ba)],
            # black and white
            [(255, 255, 255, ba), (0, 0, 0, ba)],
            #pinks and greens
            [(178, 23, 162, ba), (255, 157, 245, ba), (255, 67, 235, ba), (57, 178, 11, ba), (119, 255, 67, ba)],
            # apples!
            [(178, 22, 17, ba), (11, 178, 67, ba)],
            # Earth
            [(46, 58, 178, ba), (53, 178, 56, ba)],
            # red, pink, pink, purple, blue
            [(255, 56, 54, ba), (232, 67, 248, ba), (255, 67, 248, ba), (186, 49, 232, ba), (150, 54, 255, ba)]
        ]
    @staticmethod
    def randomColour(alpha=255):
        return (randint(0, 255), randint(0, 255), randint(0, 255), alpha)

    def complimentary(self):
        return choice(self.cols)

def brightness(colours):
    bright = 0
    for rgb in colours:
        _r, _g, _b, _ = rgb
        r = pow(_r, 2) * 0.241
        g = pow(_g, 2) * 0.691
        b = pow(_b, 2) * 0.068
        bright += sqrt(r+g+b)
    return bright / len(colours)
