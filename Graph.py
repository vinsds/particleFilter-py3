import matplotlib.pyplot as plt


def trace_graph(state_dim, state, obs, signal_type, y_label):

    for i in range(0, state_dim):
        plt.subplot(state_dim, 1, i+1)
        plt.xlabel("Time")
        plt.ylabel(str(y_label) + " n: "+str(i+1))
        # plt.title(signal_type+" n: "+str(i+1))
        plt.plot(state[i, :], 'b')
        plt.plot(obs[i, :], 'r')
    plt.show()



