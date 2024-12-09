import numpy as np
import pandas as pd
import os

from src.create_plots import create_comparative_bar_plot, create_plots_dieff, create_big_comparative_bar_plot
from src.read_data_dieff import read_raw_dieff_data
from src.read_data_timings import read_query_times, combine_means_stds, combine_runs, average_time_first_last_result, \
    make_relative, prepare_plot_data
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def create_combined_timings_plot(id_to_experiment, root_dir):
    timings = read_query_times(os.path.join(root_dir, 'data'))
    combined_mean, combined_std = combine_runs(timings, id_to_experiment)
    result = average_time_first_last_result(combined_mean)
    relative = make_relative(result)
    plot_data = prepare_plot_data(relative)
    save_location_plot = os.path.join(root_dir, 'output', 'timing_plots', 'combined_timing_plot.pdf')
    create_big_comparative_bar_plot(plot_data, save_location_plot)

def get_timings_table_data(id_to_experiment, root_dir):
    timings = read_query_times(os.path.join(root_dir, 'data'))
    combined_mean, combined_std = combine_runs(timings, id_to_experiment)

    # Experiment name to improvement data
    baseline = {}
    for template, timestamps in combined_mean['breadth-first'].items():
        timestamp_first = [query_timestamp[0] if query_timestamp else float('nan') for query_timestamp in timestamps]
        timestamp_last = [query_timestamp[-1] if query_timestamp else float('nan') for query_timestamp in timestamps]
        baseline[template] = [timestamp_first, timestamp_last]
    experiment_table_data = {}
    for experiment, template_timings in combined_mean.items():
        experiment_better_first = 0
        experiment_worse_first = 0
        experiment_better_last = 0
        experiment_worse_last = 0
        total_first = 0
        total_last = 0
        for template, timestamps in template_timings.items():
            if template != 'breadth-first':
                timestamps_first = [query_timestamp[0] if query_timestamp else float('nan') for query_timestamp in
                                   timestamps]
                timestamp_last = [query_timestamp[-1] if query_timestamp else float('nan') for query_timestamp in
                                  timestamps]
                for ts_base_first, ts_exp_first in zip(baseline[template][0], timestamps_first):
                    if ts_base_first != float('nan') and ts_exp_first != float('nan'):
                        total_first += 1
                        if ts_exp_first > 1.1 * ts_base_first:
                            experiment_worse_first += 1
                        elif ts_exp_first < .9 * ts_base_first:
                            experiment_better_first += 1
                for ts_base_last, ts_exp_last in zip(baseline[template][1], timestamp_last):
                    if ts_base_last != float('nan') and ts_exp_last != float('nan'):
                        total_last += 1
                        if ts_exp_last > 1.1 * ts_base_last:
                            experiment_worse_last += 1
                        elif ts_exp_last < .9 * ts_base_last:
                            experiment_better_last += 1
        experiment_table_data[experiment] = [100*(experiment_better_first/total_first),
                                             100*(experiment_worse_first/total_first),
                                             100*(experiment_better_last/total_last),
                                             100*(experiment_worse_last/total_last)]
    return experiment_table_data

def create_table(table_data):
    df = pd.DataFrame.from_dict(table_data, orient='index')
    columns = pd.MultiIndex.from_tuples([
        ('relRT1st', 'Better'), ('relRT1st', 'Worse'),
        ('relRTCmpl', 'Better'), ('relRTCmpl', 'Worse')
    ])

    df.columns = columns
    df_rounded = df.round(2)
    print(df_rounded)
    return df_rounded


if __name__ == "__main__":
    experiments = [
        {"type": "breadth-first", "combination": 0},
        {"type": "depth-first", "combination": 1},
        {"type": "random", "combination": 2},
        {"type": "in-degree", "combination": 3},
        {"type": "pagerank", "combination": 4},
        {"type": "rcc-1", "combination": 5},
        {"type": "rcc-2", "combination": 6},
        {"type": "rel-1", "combination": 7},
        {"type": "rel-2", "combination": 8},
        {"type": "is", "combination": 9},
        {"type": "isdcr", "combination": 10},
        {"type": "is-rcc-1", "combination": 11},
        {"type": "is-rcc-2", "combination": 12},
        {"type": "is-rel-1", "combination": 13},
        {"type": "is-rel-2", "combination": 14}
    ]
    # create_combined_timings_plot(experiments, ROOT_DIR)
    table_data_result_arrival = get_timings_table_data(experiments, ROOT_DIR)
    df_results = create_table(table_data_result_arrival)
    print(df_results.to_latex(multicolumn = True, multirow = True, float_format="%.2f"))
    # for template, timings in plot_data.items():
    #     save_location_plot = os.path.join(ROOT_DIR, 'output', 'timing_plots', '{}.pdf'.format(template))
    #     create_comparative_bar_plot(timings[2], timings[0], timings[1],
    #                                 title=template, save_location=save_location_plot)
    # data_dieff = read_raw_dieff_data(os.path.join(ROOT_DIR, 'data', 'dieff_data'))
    # create_plots_dieff(data_dieff)
    # import matplotlib.pyplot as plt
    # import numpy as np
    #
    # # Example data for plotting
    # x = np.arange(1, 6)
    # y1 = [0.3, 0.5, 0.6, 0.7, 0.4]
    # y2 = [0.4, 0.6, 0.8, 0.5, 0.3]
    #
    # # Create a figure and a grid of subplots
    # fig, axes = plt.subplots(4, 3, figsize=(17.6, 12), dpi=300)  # 4 rows, 3 columns
    #
    # # Plotting data in the first 9 subplots (3x3 grid)
    # for i in range(3):
    #     for j in range(3):
    #         axes[i, j].bar(x, y1, label="reRTCmpl", color='blue')
    #         axes[i, j].bar(x, y2, label="reRT1st", color='green', alpha=0.5)
    #         axes[i, j].set_title(f"Query Q{i * 3 + j + 1}")
    #         if j == 0:
    #             axes[i, j].set_ylabel("Score")
    #
    # # Plotting data in the last row (1 row of 2 plots)
    # axes[3, 0].bar(x, y1, label="reRTCmpl", color='blue')
    # axes[3, 0].bar(x, y2, label="reRT1st", color='green', alpha=0.5)
    # axes[3, 0].set_title("Query Q10")
    # axes[3, 0].set_ylabel("Score")
    #
    # axes[3, 1].bar(x, y1, label="reRTCmpl", color='blue')
    # axes[3, 1].bar(x, y2, label="reRT1st", color='green', alpha=0.5)
    # axes[3, 1].set_title("Query Q11")
    #
    # # Hide empty axes (for the remaining position in the grid)
    # axes[3, 2].axis('off')
    #
    # # Adjust the layout to prevent overlapping
    # plt.tight_layout()
    #
    # # Add a common legend outside the subplots
    # fig.legend(loc='upper center', ncol=2, bbox_to_anchor=(0.5, 1.05), fontsize=10)
    #
    # # Show the plot
    # plt.show()