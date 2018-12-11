from random import randint


def randomXY(imgx, imgy):
    return (randint(0, imgx-1), randint(0, imgy-1))


def randomColour(low=0, high=255, alpha=255):
    return (randint(low, high), randint(low, high), randint(low, high), alpha)
