from Observations import *
from operator import truediv
from State_functions import *
from numpy import *
from c_extends import myNormrnd


class PF:

    def __init__(self, k, n_particles, w, vect_particles, noise):
        self.k = k
        self.n_particles = n_particles
        self.w = w
        self.vect_particles = vect_particles
        self.noise = noise
        self.sys_gen_noise = noise.gen_sys_noise()

    def p_yk_given_xk(self, yk, xk, index):
        return self.noise.p_obs_noise(yk - obs_functions[index](xk, 0))

    def to_string(self):
        return "TEST PARTICLE:" \
               "\nk:       " + str(self.k)+ \
               "\nn_par:       " + str(self.n_particles)+ \
               "\nw:  " + str(self.w)+ \
               "\nvect_part:  " + str(self.vect_particles)+ \
               "\nnoise:  " + str(self.noise.view_noise_parameters()) + \
               "\n\n"

    def start(self, yk):

        k = self.k

        # check k
        if k == 0:
            print("ERRORE! K DEVE ESSERE UN INTERO MAGGIORE DI 1 O UGUALE")

        # init variable
        ns = self.n_particles       # ns = 200      ok
        nx = 1                      # nx = 1        ok

        if k == 1:
            for i in range(0, ns):
                self.vect_particles[:, i, 0] = myNormrnd.normRND(0, math.sqrt(10))

        a = truediv(1, ns)
        wkm1 = tile(a, (self.n_particles, 1))

        xkm1 = self.vect_particles[0, :, k-1]
        xkm2 = self.vect_particles[0, :, k-1]
        xkm3 = self.vect_particles[0, :, k - 1]

        xk = zeros((nx, ns))
        wk = zeros(ns)

        for n in range(0, nx):
            for i in range(0, ns):
                #xk[0, i] = state(k, xkm1[i], xkm2[i], self.noise.gen_sys_noise())
                xk[:, i] = state_functions[n](k, xkm1[i], xkm2[i], xkm3[i], self.noise.gen_sys_noise())
                wk[i] = wkm1[i, 0] * self.p_yk_given_xk(yk, xk[n, i], n)

        aux = 0

        for i in range(0, ns):
            aux += wk[i]

        wk = wk / aux

        aux_sum = 0

        for i in range(0, ns):
            aux_sum += math.pow(wk[i], 2)

        neff = 1 / aux_sum
        resample_percentage = 0.50
        nt = resample_percentage * ns

        if neff < nt:
            print('Resampling')
            [xk, wk] = self.resamlping(xk, wk, ns)

        ## fin qui tutto bene
        xhk = zeros(nx)
        wk = wk.transpose()

        for i in range(0, ns):
            xhk = xhk + wk[i] * xk[:, i]

        for t in range(0, ns):
            self.w[t, k] = wk[t]

        self.vect_particles[:, :, k] = xk[:, k]

        return xhk

    def resamlping(self, xk, wk, ns):
        dim = range(0, ns)
        #  transpose
        idx = random.choice(dim, ns, replace=True, p=wk)
        xk = xk[:, idx]
        a = truediv(1, ns)
        wk = tile(a, (1, ns))
        return [xk, wk]
