import matplotlib.pyplot as plt
import numpy as np

def create_big_comparative_bar_plot(template_to_data, save_location=None):
    mosaic = """AABB
                CCDD
                EEGG
                HHII"""
    fig, ax_dict = plt.subplot_mosaic(mosaic, figsize=(17.6, 12), sharey=True)

    exclude = ['interactive-short-1',
               'interactive-short-2',
               'interactive-short-3',
               'interactive-short-4',
               'interactive-short-5',
               'interactive-short-6']
    templates = [template for template in template_to_data.keys() if template not in exclude]
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
        ax.set_title("{}".format(template), fontsize=20)
        ax.set_xticks(ticks=x, labels=timings[2], fontsize=15, rotation=80, ha="right")
        ax.grid(axis='y', linestyle='--', linewidth=0.7, alpha=0.7)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)


    ax_dict['A'].tick_params('y', labelleft=True)
    ax_dict['C'].tick_params('y', labelleft=True)
    ax_dict['E'].tick_params('y', labelleft=True)
    ax_dict['H'].tick_params('y', labelleft=True)

    ax_dict['A'].set_ylabel('Relative Arrival Time', fontsize=14)
    ax_dict['C'].set_ylabel('Relative Arrival Time', fontsize=14)
    ax_dict['E'].set_ylabel('Relative Arrival Time', fontsize=14)
    ax_dict['H'].set_ylabel('Relative Arrival Time', fontsize=14)

    handles, labels = ax_dict['A'].get_legend_handles_labels()

    fig.legend(handles, labels, loc='upper center', fontsize=16)

    plt.tight_layout()
    if save_location:
        plt.savefig(save_location, bbox_inches='tight')
    else:
        plt.show()


def create_big_bar_plot(template_to_data, save_location=None):
    mosaic = """AABB
                CCDD
                EEGG
                HHII"""

    fig, ax_dict = plt.subplot_mosaic(mosaic, figsize=(17.6, 12), sharey=True)

    exclude = ['interactive-short-1',
               'interactive-short-2',
               'interactive-short-3',
               'interactive-short-4',
               'interactive-short-5',
               'interactive-short-6']
    templates = [template for template in template_to_data.keys() if template not in exclude]
    # for template, timings in plot_data.items():
    #     save_location_plot = os.path.join(ROOT_DIR, 'output', 'timing_plots', '{}.pdf'.format(template))
    #     create_comparative_bar_plot(timings[2], timings[0], timings[1],
    #                                 title=template, save_location=save_location_plot)

    for i, ax in enumerate(ax_dict.values()):
        template = templates[i]
        values = template_to_data[template]
        x = [i*.4 for i in np.arange(len(values[1]))]
        # Bar width
        width = 0.2
        # Create the plot
        ax.bar(x, values[0], width, color='royalblue', label='R3', edgecolor='black', alpha=1, zorder=2)

        # Adding scientific touches
        ax.set_title("{}".format(template), fontsize=20)
        ax.set_xticks(ticks=x, labels=values[1], fontsize=15, rotation=80, ha="right")
        # ax.set_yscale('log', base=2)
        ax.grid(axis='y', linestyle='--', linewidth=0.7, alpha=0.7)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    ax_dict['A'].tick_params('y', labelleft=True)
    ax_dict['C'].tick_params('y', labelleft=True)
    ax_dict['E'].tick_params('y', labelleft=True)
    ax_dict['H'].tick_params('y', labelleft=True)
    ax_dict['A'].set_ylabel('R3', fontsize=18)
    ax_dict['C'].set_ylabel('R3', fontsize=18)
    ax_dict['E'].set_ylabel('R3', fontsize=18)
    ax_dict['H'].set_ylabel('R3', fontsize=18)
    handles, labels = ax_dict['A'].get_legend_handles_labels()

    fig.legend(handles, labels, loc='upper center', fontsize=16)

    # ax_dict['D'].legend(loc='upper right', fontsize=17)

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

def horizontal_bar_plot(template_to_r3_data, template_to_timing_data, save_location = None):
    # Sample data (replace with actual values)
    exclude = ['interactive-short-1',
               'interactive-short-2',
               'interactive-short-3',
               'interactive-short-4',
               'interactive-short-5',
               'interactive-short-6']
    templates = [template for template in template_to_r3_data.keys() if template not in exclude]

    algorithms_tested = list(template_to_r3_data.values())[0][1]
    n_categories = len(algorithms_tested)

    # Bar width and spacing
    bar_width = 0.20
    group_spacing = 5  # Space between groups
    category_positions = np.arange(n_categories) # Positions of each category
    for k in range(len(category_positions)):
        category_positions[k] += group_spacing
    # Define mosaic layout
    layout = [
        ["plot1", "plot2"],
        ["plot3", "plot4"],
        ["plot5", "plot6"],
        ["plot7", "plot8"],
    ]
    max_val = 1.4
    # New color palette
    colors = ["#DB4226", "#DBC82E", "#684DDB", ]  # Black, orange, blue

    # Create the mosaic figure
    fig, axes = plt.subplot_mosaic(layout, figsize=(15, 20))

    # Generate subplots
    for i, key in enumerate(axes.keys()):
        template = templates[i]
        r3s = template_to_r3_data[template]
        timings = template_to_timing_data[template]

        ax = axes[key]

        # Adjust positions for each bar
        for idx, cat in enumerate(algorithms_tested):
            ax.barh(
                category_positions[idx] - bar_width, timings[1][idx],
                height=bar_width, color=colors[1], label='relCmpl' if idx == 0 else ""
            )
            ax.barh(
                category_positions[idx] , timings[0][idx],
                height=bar_width, color=colors[0], label='rel1st' if idx == 0 else ""
            )
            ax.barh(
                category_positions[idx] + bar_width, r3s[0][idx],
                height=bar_width, color=colors[2], label='$R^{3}$' if idx == 0 else ""
            )

        # Format axes
        ax.set_yticks(category_positions)
        ax.yaxis.set_label_position("right"),
        ax.set_yticklabels(algorithms_tested if i % 2 == 0 else [], size=18)
        ax.set_title(templates[i], size=18, fontweight='bold', pad=-200)
        if i == 6 or i == 7:
            ax.set_xlabel("Relative Result Arrival Time (s) / \n $R^3$", size=16)
        ax.grid(axis='x', linestyle='--', linewidth=0.5, alpha=0.7)  # Add gridlines
        ax.tick_params(axis='x', labelsize=16)
        if i % 2 == 0:
            ax.tick_params(axis='y', labelleft=False, labelright=True, left=False, right=True)
            for label in ax.get_yticklabels():
                label.set_horizontalalignment('center')
                label.set_x(1.13)
            left, right = ax.get_xlim()
            ax.set_xlim(max_val, 0)
            ax.spines['left'].set_visible(False)
        else:
            ax.set_xlim(0, max_val)
            ax.tick_params(axis='y', labelleft=False, labelright=False, right=False, left=True)
            ax.spines['right'].set_visible(False)
        # Add legend to the first subplot only
        if i == 6:
            handles, labels = ax.get_legend_handles_labels()
            print(handles)
            order = [2, 1, 0]
            ax.legend([handles[idx] for idx in order],
                      [labels[idx] for idx in order],
                      loc="upper left", fontsize='xx-large')

        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)

    # Adjust layout
    plt.tight_layout()
    if save_location:
        plt.savefig(save_location, bbox_inches='tight')
    else:
        plt.show()

if __name__ == '__main__':
    pass
    # horizontal_bar_plot()
