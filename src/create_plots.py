import matplotlib.pyplot as plt
import numpy as np

def create_big_comparative_bar_plot(template_to_data, save_location=None):
    mosaic = """AABBCC
                DDEEFF
                GGHHII
                .JJKK."""
    fig, axes = plt.subplots(4, 3, figsize=(17.6, 12), dpi=300)  # 4 rows, 3 columns
    fig, ax_dict = plt.subplot_mosaic(mosaic, figsize=(17.6, 12), sharey=True)

    timed_out = ['interactive-short-2', 'interactive-short-3', 'interactive-short-6']
    templates = [template for template in template_to_data.keys() if template not in timed_out]
    # for template, timings in plot_data.items():
    #     save_location_plot = os.path.join(ROOT_DIR, 'output', 'timing_plots', '{}.pdf'.format(template))
    #     create_comparative_bar_plot(timings[2], timings[0], timings[1],
    #                                 title=template, save_location=save_location_plot)

    for i, ax in enumerate(ax_dict.values()):
        template = templates[i]
        timings = template_to_data[template]
        x = [i*.4 for i in np.arange(len(timings[2]))]
        # Bar width
        width = 0.2
        # Create the plot
        ax.bar(x, timings[0], width, color='royalblue', label='relRT1st', edgecolor='black', alpha=1, zorder=2)
        ax.bar(x, timings[1], width, color='orange', label='relRTCmpl', edgecolor='black', alpha=1, zorder=1)

        # Adding scientific touches
        ax.set_title("{}".format(template), fontsize=14)
        ax.set_xticks(ticks=x, labels=timings[2], fontsize=10, rotation=80, ha="right")
        ax.grid(axis='y', linestyle='--', linewidth=0.7, alpha=0.7)

    ax_dict['D'].tick_params('y', labelleft=True)
    ax_dict['G'].tick_params('y', labelleft=True)
    ax_dict['J'].tick_params('y', labelleft=True)
    ax_dict['J'].set_ylabel('Relative Arrival Time', fontsize=12)
    ax_dict['D'].set_ylabel('Relative Arrival Time', fontsize=12)
    ax_dict['G'].set_ylabel('Relative Arrival Time', fontsize=12)
    ax_dict['A'].legend(loc='upper left', fontsize=10)

    plt.tight_layout()
    if save_location:
        plt.savefig(save_location, bbox_inches='tight')
    else:
        plt.show()



def create_comparative_bar_plot(categories, time_first, time_last, title='Comparative Bar Plot', save_location=None):
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
    plt.bar(x, time_first, width, color='royalblue', label='relRT1st', edgecolor='black', alpha=1, zorder=2)
    plt.bar(x, time_last, width, color='orange', label='relRTCCmpl', edgecolor='black', alpha=1, zorder=1)

    # Adding scientific touches
    plt.title(title, fontsize=14, weight='bold')
    plt.xlabel('Categories', fontsize=10)
    plt.ylabel('Values', fontsize=12)
    plt.xticks(ticks=x, labels=categories, fontsize=10, rotation=45, ha="right")
    plt.grid(axis='y', linestyle='--', linewidth=0.7, alpha=0.7)
    plt.legend(fontsize=10, frameon=False)
    plt.tight_layout()

    if save_location:
        plt.savefig(save_location)
    # Display the plot
    plt.show()


def create_plots_dieff(data_dieff):
    for experiment in data_dieff.keys():
        for template in data_dieff[experiment].keys():
            result = data_dieff[experiment][template]
            retrieval_dieff_result = result['retrievalDieff']
            result_dieff_result = result['resultDieff']

            for i in range(len(result_dieff_result)):
                x1 = result_dieff_result[i]['linSpace']
                y1 = result_dieff_result[i]['answerDistributionFunction']
                x2 = retrieval_dieff_result[i]['linSpace']
                y2 = retrieval_dieff_result[i]['answerDistributionFunction']
                plot_retrieval_and_result_dieff(x1, y1, x2, y2, ['Result', 'Retrieval'],
                                                ['blue', 'red'],
                                                xlabel='Time(ms)', ylabel='Results',
                                                title='{}.{}'.format(template, i))    # # Example usage
    # data = [
    #     [0, 500, 1500, 3000, 4000, 5000],  # Line 1 (y-values)
    #     [0, 300, 1200, 2500, 3500, 4900],  # Line 2 (y-values)
    #     [0, 100, 800, 2000, 3000, 4500],  # Line 3 (y-values)
    # ]
    # labels = ['nLDE Not Adaptive', 'nLDE Selective', 'nLDE Random']
    # colors = ['blue', 'gray', 'lightgray']
    # plot_multiple_lines(data, labels, colors, xlabel='Time', ylabel='# Answers Produced',
    #                     title='Answer Distribution')


def plot_retrieval_and_result_dieff(x1, y1, x2, y2, labels, colors, xlabel, ylabel, title):
    """
    Plot two lines with given x, y values and customize the plot.

    Parameters:
        x1, y1 (list): X and Y values for the first line.
        x2, y2 (list): X and Y values for the second line.
        labels (list): A list of two strings for the legend labels.
        colors (list): A list of two colors for the lines.
        xlabel (str): Label for the x-axis.
        ylabel (str): Label for the y-axis.
        title (str): Title of the plot.
    """
    plt.figure(figsize=(8, 6))  # Set figure size

    # Plot the first line
    plt.plot(x1, y1, label=labels[0], color=colors[0], linewidth=2)

    # Plot the second line
    plt.plot(x2, y2, label=labels[1], color=colors[1], linewidth=2)

    # Add labels, title, and legend
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend(loc='upper left')

    # Add grid and display the plot
    plt.grid(alpha=0.5)
    plt.show()


# # Example input
# x1 = [0, 1, 2, 3, 4]
# y1 = [0, 1, 4, 9, 16]
# x2 = [0, 1, 2, 3, 4]
# y2 = [16, 9, 4, 1, 0]
# labels = ['Increasing', 'Decreasing']
# colors = ['blue', 'red']
#
# # Call the function to plot
# plot_two_lines(x1, y1, x2, y2, labels, colors, xlabel='X-Axis', ylabel='Y-Axis', title='Two Line Plot')
