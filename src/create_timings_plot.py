import os
import numpy as np

from main import ROOT_DIR
from src.create_plots import create_big_comparative_bar_plot, create_big_bar_plot, horizontal_bar_plot
from src.read_data_dieff import read_raw_metric_data
from src.read_data_timings import read_query_times, combine_runs, average_time_first_last_result, make_relative, \
    prepare_plot_data, prepare_single_run, combine_runs_rel, prepare_plot_data_corrected


def create_horizontal_combined_plot(id_to_experiment, root_dir, save_location_plot=None):
    r3_metrics_raw = read_raw_metric_data(os.path.join(root_dir, 'data_bak', 'r3_data'))
    r3_metrics_raw_sorted = dict(sorted(r3_metrics_raw.items()))
    data_per_algorithm_raw = {id_to_experiment[int(key)]['type']: value for key, value in r3_metrics_raw_sorted.items()}
    plot_r3_data = group_per_template(data_per_algorithm_raw, 'unweighted')

    timings = read_query_times(os.path.join(root_dir, 'data'))
    combine_runs(timings, id_to_experiment)
    combined_mean, combined_std = combine_runs(timings, id_to_experiment)
    result = average_time_first_last_result(combined_mean)
    relative = make_relative(result)
    plot_timing_data = prepare_plot_data(relative)
    horizontal_bar_plot(plot_r3_data, plot_timing_data, save_location_plot)

def group_per_template(metric_data, metric_name):
    output = {}
    for template, timings in list(metric_data.values())[0].items():
        template_metric_values = []
        template_experiments = []
        for experiment in metric_data.keys():
            total = 0
            n = 0
            for query in metric_data[experiment][template][metric_name]:
                for repetition in query:
                    if repetition != -1:
                        total += repetition
                        n += 1
            if n > 0:
                template_metric_values.append(total / n)
            else:
                template_metric_values.append(0)
            template_experiments.append(experiment)
        output[template] = [template_metric_values, template_experiments]
    return output


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
        {"type": "is-rel-2", "combination": 14},
        {"type": "type-index", "combination": 15},
        {"type": "oracle", "combination": 16}
    ]

    save_location_horizontal_plot = os.path.join(ROOT_DIR, 'output', 'plots', 'combined_r3_timings_plot.pdf')
    create_horizontal_combined_plot(experiments, ROOT_DIR, save_location_horizontal_plot)
