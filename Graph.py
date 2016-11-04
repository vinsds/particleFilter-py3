import matplotlib.pyplot as plt


def trace_graph(state_dim, signal_1, signal_2, signal_type):

    for i in range(0, state_dim):
        plt.subplot(state_dim, 1, i+1)
        plt.xlabel("Time")
        plt.ylabel(signal_type+" n: "+str(i+1))
        plt.plot(signal_1[i, :], 'b')
        plt.plot(signal_2[i, :], 'r')
    plt.show()


