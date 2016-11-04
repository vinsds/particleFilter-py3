from numpy import *


def obs(x, v):
    if v == '':
        v = 0
    x = math.pow(x, 2)
    return x / 20 + v
