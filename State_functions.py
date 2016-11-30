from numpy import *

state_functions = [

    lambda k, xkm1, xkm2, xkm3, uk: xkm1 / 2 + 25 * xkm2 / (1 + math.pow(xkm2, 2)) + 8 * cos(1.2 * k) + uk,
    lambda k, xkm1, xkm2, xkm3, uk: xkm2 + 10 * xkm3/(1+ math.pow(xkm3, 2)) + 4*cos(1.2*k) + uk,
    # lambda k, xkm1, xkm2, xkm3, uk: xkm1 / 2 + 25 * xkm2 / (1 + math.pow(xkm2, 2)) + 8 * cos(1.2 * k) + uk
    # lambda k, xkm1, xkm2, xkm3, uk: xkm1 / 2 + 25 * xkm2 / (1 + math.pow(xkm2, 2)) + 8 * sin(1.2 * k) + uk
    lambda k, xkm1, xkm2, xkm3, uk: xkm1 / 2 + 25 * xkm2 / (1 + math.pow(xkm2, 2)) + 8 * cos(1.2 * k) + uk,
    # lambda k, xkm1, xkm2, xkm3, uk: xkm1 / 2 + 25 * xkm2 / (1 + math.pow(xkm2, 2)) + 8 * cos(1.2 * k) + uk
]

