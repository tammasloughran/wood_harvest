# Plot results
import matplotlib.pyplot as plt


def plot_wood(years, history, access, ylabel, title)->None:
    """Plot the results of the wood harvest sub model against ACCESS.
    years - array of years for the x axis
    history - 1D global sum array of history to plot
    access - 1D global sum from ACCESS
    ylabel - the y label
    title - the title
    """
    plt.figure()
    plt.plot(years, history, label='python')
    plt.plot(years, access, label='ACCESS')
    plt.xlabel('Year')
    plt.ylabel(ylabel)
    plt.legend()
    plt.title(title)

