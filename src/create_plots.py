import matplotlib
import matplotlib.pyplot as plt
import numpy as np


def create_comparative_bar_plot(categories, time_first, time_last, title='Comparative Bar Plot'):
    """
    Creates a bar plot comparing two datasets side by side for each category.

    Parameters:
    - categories: List of category labels.
    - values_1: List of values for the first dataset.
    - values_2: List of values for the second dataset.
    - title: Title of the plot (default is 'Comparative Bar Plot').
    """
    # X-axis positions
    x = np.arange(len(categories))

    # Bar width
    width = 0.4

    # Create the plot
    plt.bar(x, time_first, width, color='royalblue', label='relRTCCmpl' , edgecolor='black', alpha=.5)
    plt.bar(x, time_last, width, color='orange', label='relRT1st', edgecolor='black', alpha=1)

    # Adding scientific touches
    plt.title(title, fontsize=14, weight='bold')
    plt.xlabel('Categories', fontsize=12)
    plt.ylabel('Values', fontsize=12)
    plt.xticks(ticks=x, labels=categories, fontsize=10)
    plt.grid(axis='y', linestyle='--', linewidth=0.7, alpha=0.7)
    plt.legend(fontsize=10, frameon=False)
    plt.tight_layout()

    # Display the plot
    plt.show()


