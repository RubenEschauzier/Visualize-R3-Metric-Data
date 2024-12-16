import os
import numpy as np

from main import ROOT_DIR
from src.create_plots import create_big_comparative_bar_plot, create_big_bar_plot
from src.read_data_dieff import read_raw_metric_data
from src.read_data_timings import read_query_times, combine_runs, average_time_first_last_result, make_relative, \
    prepare_plot_data, prepare_single_run, combine_runs_test, prepare_plot_data_corrected


def create_combined_timings_plot(id_to_experiment, root_dir, save_location_plot=None):
    timings = read_query_times(os.path.join(root_dir, 'data'))
    combine_runs_test(timings, id_to_experiment, 180_000)
    combined_mean, combined_std = combine_runs(timings, id_to_experiment)
    result = average_time_first_last_result(combined_mean)
    relative = make_relative(result)
    plot_data = prepare_plot_data(relative)
    create_big_comparative_bar_plot(plot_data, save_location_plot)

def create_combined_timings_plot_corrected(id_to_experiment, root_dir, save_location_plot=None):
    timings = read_query_times(os.path.join(root_dir, 'data'))
    combined_rel1st, combined_relcmpl = combine_runs_test(timings, id_to_experiment, 180_000)
    plot_data = prepare_plot_data_corrected(combined_rel1st, combined_relcmpl)
    create_big_comparative_bar_plot(plot_data, save_location_plot)

def create_combined_timings_plot_single_run(id_to_experiment, root_dir, save_location_plot=None):
    timings = read_query_times(os.path.join(root_dir, 'data'))
    single_run_data = prepare_single_run(timings, id_to_experiment, 0)

def create_r3_values_plot(id_to_experiment, root_dir, save_location_plot=None):
    r3_metrics_raw = read_raw_metric_data(os.path.join(root_dir, 'data', 'r3_data'))
    r3_metrics_raw_sorted = dict(sorted(r3_metrics_raw.items()))
    data_per_algorithm_raw = {id_to_experiment[int(key)]['type']: value for key, value in r3_metrics_raw_sorted.items()}
    grouped_metrics = group_per_template(data_per_algorithm_raw, 'unweighted')
    create_big_bar_plot(grouped_metrics, save_location_plot)


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
        {"type": "oracle", "combination": 15}
    ]
    # create_combined_timings_plot_single_run(experiments, ROOT_DIR)
    save_location_timings_plot = os.path.join(ROOT_DIR, 'output', 'timing_plots', 'combined_timing_plot.pdf')
    create_combined_timings_plot_corrected(experiments, ROOT_DIR, save_location_timings_plot)

    # CONSIDER MAKING THIS A LOG2 PLOT AS IN PREVIOUS PAPER
    save_location_r3_plot = os.path.join(ROOT_DIR, 'output', 'timing_plots', 'combined_r3_plot.pdf')
    create_r3_values_plot(experiments, ROOT_DIR, save_location_r3_plot)
