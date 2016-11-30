from numpy import *
from c_extends import myPdf
from c_extends import myNormrnd


class Noise:

    def __init__(self, nu, nv, sigma_u, sigma_v):

        #dimensione del vettore di rumore di processo
        self.nu = nu

        #dimensione del vettore di rumore delle osservazioni
        self.nv = nv

        #deviazione standard dello stato
        self.sigma_u = math.sqrt(sigma_u)

        #deviazione standard dell'osservazione
        self.sigma_v = math.sqrt(sigma_v)


    #Calcolo della sigma_u
    # def calculate_sigma_u(self, value):
    #     self.sigma_u = math.sqrt(value)
    #
    # #Calcolo della sigma_v
    # def calculate_sigma_v(self, value):
    #     self.sigma_v = math.sqrt(value)

    #Generazione del rumore di stato
    def gen_sys_noise(self):
        sigma_u = self.sigma_u
        return myNormrnd.normRND(0, sigma_u)


    #PDF del rumore delle osservazioni
    def p_obs_noise(self, v):
        if v == '':
            v = 1
        sigma_v = self.sigma_v
        return myPdf.pdf(v, 0, sigma_v)

    #Generazione del rumore delle osservazioni
    def gen_obs_noise(self):
        sigma_v = self.sigma_v
        return myNormrnd.normRND(0, sigma_v)

    # to_string
    # def view_noise_parameters(self):
    #     return "NOISE PARAMTERS:" \
    #            "\nnu:       " + str(self.nu)+\
    #            "\nnv:       " + str(self.nv)+ \
    #            "\nsigma_u:  " + str(self.sigma_u)+\
    #            "\nsigma_v:  " + str(self.sigma_v)+ \
    #            "\n\n"
