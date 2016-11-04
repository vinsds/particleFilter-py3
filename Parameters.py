class Parameters:

    # Constructor
    # @state_dim define the state dimension
    # @particles define the particles number
    # @time define the simulation time
    def __init__(self, state_dim, particles, time):
        self.state_dim = state_dim
        self.particles = particles
        self.time = time