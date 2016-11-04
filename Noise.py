from numpy import *
from c_extends import myPdf
from c_extends import myNormrnd

class Noise:

    def __init__(self, nu, nv, sigma_u, sigma_v):
        self.nu = nu
        self.nv = nv
        self.sigma_u = math.sqrt(sigma_u)
        self.sigma_v = math.sqrt(sigma_v)

    # size of the vector of process and observation noise
    def calculate_sigma_u(self, value):
        self.sigma_u = math.sqrt(value)

    # size of the vector of process and observation noise
    def calculate_sigma_v(self, value):
        self.sigma_v = math.sqrt(value)

    def gen_sys_noise(self):
        sigma_u = self.sigma_u
        return myNormrnd.normRND(0, sigma_u)


    # PDF of observation noise and noise generator function
    def p_obs_noise(self, v):
        if v == '':
            v = 1
        sigma_v = self.sigma_v
        return myPdf.pdf(v, 0, sigma_v)

    def gen_obs_noise(self):
        sigma_v = self.sigma_v
        return myNormrnd.normRND(0, sigma_v)

    # to_string
    def view_noise_parameters(self):
        return "NOISE PARAMTERS:" \
               "\nnu:       " + str(self.nu)+\
               "\nnv:       " + str(self.nv)+ \
               "\nsigma_u:  " + str(self.sigma_u)+\
               "\nsigma_v:  " + str(self.sigma_v)+ \
               "\n\n"
