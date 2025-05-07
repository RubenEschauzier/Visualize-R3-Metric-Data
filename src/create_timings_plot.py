import ast
import math
import os
import numpy as np

from main import ROOT_DIR
from src.create_plots import create_big_comparative_bar_plot, create_big_bar_plot, horizontal_bar_plot, \
    horizontal_bar_plot_reduced
from src.read_data_dieff import read_raw_metric_data
from src.read_data_timings import read_query_times, combine_runs, average_time_first_last_result, make_relative, \
    prepare_plot_data, prepare_single_run, combine_runs_rel, prepare_plot_data_corrected, read_query_times_single_run, \
    prepare_plot_data_results


def create_horizontal_combined_plot(id_to_experiment, root_dir, save_location_plot=None):
    r3_metrics_raw = read_raw_metric_data(os.path.join(root_dir, 'data_bak', 'r3_data'))
    r3_metrics_raw_sorted = dict(sorted(r3_metrics_raw.items()))
    data_per_algorithm_raw = {id_to_experiment[int(key)]['type']: value for key, value in r3_metrics_raw_sorted.items()}
    plot_r3_data = group_per_template(data_per_algorithm_raw, 'unweighted')

    timings = read_query_times(os.path.join(root_dir, 'data_bak'))
    combine_runs(timings, id_to_experiment)
    combined_mean, combined_std = combine_runs(timings, id_to_experiment)
    result = average_time_first_last_result(combined_mean)
    relative = make_relative(result)
    plot_timing_data = prepare_plot_data(relative)
    horizontal_bar_plot(plot_r3_data, plot_timing_data, save_location_plot)

def create_horizontal_combined_plot_single_run(id_to_experiment, root_dir, save_location_plot=None):
    r3_metrics_raw = read_raw_metric_data(os.path.join(root_dir, 'data', 'r3-metrics'))
    r3_metrics_raw_sorted = dict(sorted(r3_metrics_raw.items()))
    data_per_algorithm_raw = {id_to_experiment[int(key)]['type']: value for key, value in r3_metrics_raw_sorted.items()}
    plot_r3_data = group_per_template(data_per_algorithm_raw, 'unweighted')

    timings = read_query_times_single_run(os.path.join(root_dir, 'data', 'timings'))
    timings_named = index_to_experiment_name(timings, id_to_experiment)
    timestamps, number_results = extract_single_run_timestamps(timings_named)
    result = average_instantiations(timestamps)
    average_number_results = average_results(number_results)

    relative, relative_results = make_relative(result, average_number_results)
    plot_timing_data = prepare_plot_data(relative)
    plot_result_data = prepare_plot_data_results(relative_results)
    horizontal_bar_plot(plot_r3_data, plot_timing_data, plot_result_data, save_location_plot)

def create_horizontal_combined_plot_single_run_non_relative(id_to_experiment, root_dir, save_location_plot=None):
    expect_order = ['breadth-first', 'depth-first', 'random', 'in-degree', 'pagerank', 'rcc-1', 'rcc-2', 'rel-1',
                    'rel-2', 'is', 'isdcr', 'is-rcc-1', 'is-rcc-2', 'is-rel-1', 'is-rel-2', 'type-index', 'oracle']

    r3_metrics_raw = read_raw_metric_data(os.path.join(root_dir, 'data', 'r3-metrics'))
    r3_metrics_raw_sorted = dict(sorted(r3_metrics_raw.items()))
    data_per_algorithm_raw = {id_to_experiment[int(key)]['type']: value for key, value in r3_metrics_raw_sorted.items()}
    plot_r3_data = group_per_template(data_per_algorithm_raw, 'unweighted')
    validate_order(plot_r3_data, expect_order, 1)

    timings = read_query_times_single_run(os.path.join(root_dir, 'data', 'timings'))
    timings_named = index_to_experiment_name(timings, id_to_experiment)
    timestamps, number_results = extract_single_run_timestamps(timings_named)
    std = extract_single_run_standard_deviation(timings_named)
    result = average_instantiations(timestamps)
    combined_std = calculate_std_mean(timestamps, std, result)
    plot_std_data = prepare_plot_data(combined_std, expect_order)

    average_number_results = average_results(number_results)
    relative, relative_results = make_relative(result, average_number_results)

    plot_timing_data = prepare_plot_data(result, expect_order)
    plot_result_data = prepare_plot_data_results(average_number_results, expect_order)
    plot_result_data_relative = prepare_plot_data_results(relative_results, expect_order)
    validate_order(plot_result_data, expect_order, -1)
    validate_order(plot_result_data_relative, expect_order, -1)

    horizontal_bar_plot(plot_r3_data, plot_timing_data,
                        plot_result_data=plot_result_data_relative,
                        save_location=save_location_plot[0],
                        template_to_timing_std=plot_std_data)
    horizontal_bar_plot_reduced(plot_r3_data, plot_timing_data,
                        plot_result_data=plot_result_data_relative,
                        save_location=save_location_plot[1],
                        template_to_timing_std=plot_std_data)

    pass
def validate_order(plot_data, expected_order, algorithm_index):
    for template, data in plot_data.items():
        # the index passed should be the algorithms belonging to each datapoint.
        print(data[algorithm_index])
        print(expected_order)
        assert data[algorithm_index] == expected_order


def calculate_std_mean(timestamps, timestamps_std, average_first_last_timestamp):
    output_timestamp_std = {}
    for experiment in timestamps.keys():
        experiment_std = {}
        for template in timestamps[experiment].keys():
            template_timestamps = timestamps[experiment][template]
            template_timestamps_std = timestamps_std[experiment][template]
            first, last = average_first_last_timestamp[experiment][template]
            n_instantiations = len(timestamps[experiment][template])
            first_std, last_std = 0, 0
            for i in range(len(template_timestamps)):
                instantiation_timestamps = template_timestamps[i]
                instantiation_timestamps_std = template_timestamps_std[i]
                if len(instantiation_timestamps)>0:
                    first_std += (instantiation_timestamps_std[0] + (instantiation_timestamps[0] - first)**2)
                    last_std += (instantiation_timestamps[-1] + (instantiation_timestamps[-1] - last)**2)
            experiment_std[template] = [math.sqrt(first_std / n_instantiations), math.sqrt(last_std / n_instantiations)]
        output_timestamp_std[experiment] = experiment_std
    return output_timestamp_std

# def element_wise_mean(data):
#     max_timestamps = max([len(instantiation) for instantiation in data])
#     print(max_timestamps)
#
#     total_value = [0] * max_timestamps
#     total_n = [0] * max_timestamps
#     for instantiation in data:
#         for i, timestamp in enumerate(instantiation):
#             total_value[i] += timestamp
#             total_n[i] += 1
#     output = [total_time / n for n, total_time in zip(total_n, total_value)]
#     return  output

def index_to_experiment_name(data, experiment_names):
    output = {}
    for key, value in data.items():
        output[experiment_names[key]["type"]] = value
    return output

def extract_single_run_timestamps(data):
    output = {}
    output_results = {}
    for key, value in data.items():
        experiment_output = {}
        experiment_output_results = {}
        grouped_per_template = value.groupby('name')['timestamps'].agg(list).to_dict()
        grouped_per_template_results = value.groupby('name')['results'].agg(list).to_dict()

        for template, timestamps in grouped_per_template.items():
            # MS to S
            timestamps_as_list = [
                [float(x)/1000 for x in s.split()] if isinstance(s, str) or not math.isnan(s) else []
                for s in timestamps
            ]
            experiment_output[template] = timestamps_as_list
            experiment_output_results[template] = grouped_per_template_results[template]
        output[key] = experiment_output
        output_results[key] = experiment_output_results
    return output, output_results

def extract_single_run_standard_deviation(data):
    output = {}
    for key, value in data.items():
        experiment_output = {}
        grouped_per_template = value.groupby('name')['timestampsStd'].agg(list).to_dict()

        for template, timestamps in grouped_per_template.items():
            # MS to S
            timestamps_as_list = [
                [float(x)/1000 for x in s.split()] if isinstance(s, str) or not math.isnan(s) else []
                for s in timestamps
            ]
            experiment_output[template] = timestamps_as_list
        output[key] = experiment_output
    return output


def average_instantiations(data):
    output = {}
    for experiment, templates in data.items():
        experiment_output = {}
        total_first = 0
        total_last = 0
        for template, timestamps in templates.items():
            n = 0
            for timestamp_instantiation in timestamps:
                if len(timestamp_instantiation) > 0:
                    total_first += timestamp_instantiation[0]
                    total_last += timestamp_instantiation[-1]
                    n += 1
            experiment_output[template] = [total_first / n, total_last / n]
        output[experiment] = experiment_output
    return output

def average_results(results_data):
    output = {}
    for experiment, templates in results_data.items():
        experiment_output = {}
        for template, results in templates.items():
            experiment_output[template] = np.mean(results)
        output[experiment] = experiment_output
    return output


def group_per_template(metric_data, metric_name):
    output = {}
    for template, timings in list(metric_data.values())[0].items():
        template_metric_values = []
        template_metric_std = []
        template_experiments = []
        for experiment in metric_data.keys():
            total = 0
            n = 0
            all_template_values = []
            for query in metric_data[experiment][template][metric_name]:
                all_template_values.extend(query)
                for repetition in query:
                    if repetition != -1:
                        total += repetition
                        n += 1
            if n > 0:
                template_metric_values.append(total / n)
                template_metric_std.append(np.std(all_template_values))
            else:
                template_metric_values.append(0)
            template_experiments.append(experiment)
        output[template] = [template_metric_values, template_experiments, template_metric_std]
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
        {"type": "oracle", "combination": 16 }
    ]

    # save_location_horizontal_plot = os.path.join(ROOT_DIR, 'output', 'plots', 'combined_r3_timings_plot.pdf')
    # create_horizontal_combined_plot(experiments, ROOT_DIR, save_location_horizontal_plot)

    # save_location_horizontal_plot_updated = os.path.join(ROOT_DIR, 'output', 'plots',
    #                                                      'combined_r3_timings_plot_updated.pdf')
    # create_horizontal_combined_plot_single_run(experiments, ROOT_DIR, save_location_horizontal_plot_updated)

    save_location_horizontal_plot_updated = os.path.join(ROOT_DIR, 'output', 'plots',
                                                         'combined_r3_timings_plot_non_relative.pdf')
    save_location_horizontal_plot_updated_reduced = os.path.join(ROOT_DIR, 'output', 'plots',
                                                         'combined_r3_timings_plot_non_relative_reduced.pdf')

    create_horizontal_combined_plot_single_run_non_relative(
        experiments, ROOT_DIR,
        [save_location_horizontal_plot_updated, save_location_horizontal_plot_updated_reduced])
