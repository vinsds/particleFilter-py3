from Parameters import *
from Noise import *
from PF import *
from State_functions import *

'''
Set DEBUG true to show the operations results
'''
DEBUG = False


# Define system parameters and observation time
STATE_DIM = 3
PARTICLES = 200
TIME = 50

sys_par = Parameters(
    STATE_DIM,
    PARTICLES,
    TIME
)

# Define Noise parameters
SIGMA_U = 1
SIGMA_V = 10

noise = Noise(
    sys_par.state_dim,
    sys_par.state_dim,
    SIGMA_U,
    SIGMA_V
    )

'''
Separate memory space
'''
x = zeros((sys_par.state_dim, TIME))
y = zeros((sys_par.state_dim, TIME))
u = zeros((sys_par.state_dim, TIME))
v = zeros((sys_par.state_dim, TIME))

# Initial state
xh0 = 0

for index in range(0, sys_par.state_dim):
            u[index, 0] = xh0
            v[index, 0] = noise.gen_obs_noise()
            x[index, 0] = xh0
            y[index, 0] = obs_functions[index](x[index, 0], v[index, 0])


for t in range(1, sys_par.time):
    for index in range(0, sys_par.state_dim):
        u[index, t] = noise.gen_sys_noise()
        v[index, t] = noise.gen_obs_noise()
        x[index, t] = state_functions[index](t, x[0, t-1], x[1, t-1], x[2, t-1], u[index, t-1])
        y[index, t] = obs_functions[index](x[index, t], v[index, t])


'''
Preparing memory
'''
xh = zeros((sys_par.state_dim, TIME))
yh = zeros((sys_par.state_dim, TIME))

'''
Init filtering
'''

k = 1
n_particles = 200
w = zeros((n_particles, TIME))
vect_particles = zeros((1, n_particles, TIME))

test_filter = PF(
    k,
    n_particles,
    w,
    vect_particles,
    noise
)

for n in range(0, sys_par.state_dim):
    for k in range(1, sys_par.time):
        test_filter.k = k
        xh[n, k] = test_filter.start(y[n, k])
        yh[n, k] = obs_functions[n](xh[n, k], 0)





