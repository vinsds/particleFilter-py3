from numpy import *


def state(k, xkm1, xkm2, uk):
    result = xkm1 / 2 + 25 * xkm2 / (1 + math.pow(xkm2, 2)) + 8 * math.cos(1.2 * k) + uk
    return result


