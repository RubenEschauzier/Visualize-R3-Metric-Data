import os
from typing import Literal

import pandas as pd
import copy

from main import ROOT_DIR
from src.create_timings_plot import index_to_experiment_name, extract_single_run_timestamps
from src.read_data_dieff import read_raw_metric_data
from src.read_data_timings import read_query_times, combine_runs, combine_runs_rel, read_query_times_single_run


def read_timings_data(id_to_experiment, root_dir):
    timings = read_query_times(os.path.join(root_dir, 'data'))
    combined_mean, combined_std = combine_runs(timings, id_to_experiment)
    return combined_mean, combined_std

def read_timings_data_single_run(id_to_experiment, root_dir):
    timings = read_query_times_single_run(os.path.join(root_dir, 'data', 'timings'))
    timings_named = index_to_experiment_name(timings, id_to_experiment)
    timestamps, results = extract_single_run_timestamps(timings_named)
    return timestamps, []

def get_timings_table_data(combined_mean, combined_std):
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

def create_table(table_data, metric_names):
    df = pd.DataFrame.from_dict(table_data, orient='index')
    columns = pd.MultiIndex.from_tuples([
        (metric_names[0], 'Better'), (metric_names[0], 'Worse'),
        (metric_names[1], 'Better'), (metric_names[1], 'Worse')
    ])

    df.columns = columns
    df_rounded = df.round(2)
    return df_rounded

def create_metrics_table_data(experiment_data, direction_better: Literal['lower', 'higher']):
    baseline = experiment_data['breadth-first']
    table_data = {}
    for experiment, data in experiment_data.items():
        if experiment != 'breadth-first':
            better, worse = compare_to_baseline(baseline, experiment_data[experiment], direction_better)
            experiment_comparison_data = []
            for i in range(len(better)):
                experiment_comparison_data.append(better[i])
                experiment_comparison_data.append(worse[i])
            table_data[experiment] = experiment_comparison_data
    return table_data

def compare_to_baseline(baseline, template_metrics, direction_better: Literal['lower', 'higher']):
    # List on a per metric basis, so first element is # times that for first metric it is better
    n = len(template_metrics[list(template_metrics.keys())[0]])
    experiments_better = [0 for i in range(n)]
    experiments_worse = [0 for i in range(n)]
    total = [0 for i in range(n)]
    for template, metrics in template_metrics.items():
        for i in range(len(metrics)):
            for (val_baseline, val_compare) in zip(baseline[template][i], metrics[i]):
                if val_compare != float('nan') and val_baseline != float('nan'):
                    total[i] += 1
                    if direction_better == 'higher':
                        if val_compare > 1.1 * val_baseline:
                            experiments_better[i] += 1
                        elif val_compare < .9 * val_baseline:
                            experiments_worse[i] += 1
                    if direction_better == 'lower':
                        if val_compare > 1.1 * val_baseline:
                            experiments_worse[i] += 1
                        elif val_compare < .9 * val_baseline:
                            experiments_better[i] += 1



    percentage_better = [100*(experiments_better[i]/total[i]) for i in range(n)]
    percentage_worse = [100*(experiments_worse[i]/total[i]) for i in range(n)]

    return percentage_better, percentage_worse

def extract_dieff_metrics(data_dieff):
    output = {}
    for experiment, data in data_dieff.items():
        experiment_metrics = {}
        for template, metrics in data.items():
            template_metrics = {}
            for metric in metrics.keys():
                if metric != 'totalExecutionTime':
                    template_metrics[metric] = [[x['dieff']] for x in metrics[metric]]
                pass
            experiment_metrics[template] = template_metrics
        output[experiment] = experiment_metrics
    return output

def process_metrics_into_list(data_experiments, invalid_values):
    output_list = {}
    for experiment, output in data_experiments.items():
        experiment_output_list = {}
        for template, template_metrics in output.items():
            metric_list = []
            for metric in template_metrics.keys():
                filtered_metrics = [[x for x in repetitions if x not in invalid_values ] for repetitions in template_metrics[metric]]
                averaged_metrics = [sum(repetitions)/len(repetitions) if len(repetitions) > 0 else float('nan')
                                    for repetitions in filtered_metrics]
                metric_list.append(averaged_metrics)
            experiment_output_list[template] = metric_list
        output_list[experiment] = experiment_output_list
    return output_list

def create_r3_table(id_to_experiment, root_dir, path_to_metric_data, metric_names):
    path = os.path.join(root_dir, path_to_metric_data)
    raw_data = read_raw_metric_data(path)
    raw_data_sorted = dict(sorted(raw_data.items()))

    data_per_algorithm = {id_to_experiment[int(key)]['type']: value for key, value in raw_data_sorted.items()}
    data_per_algorithm_list = process_metrics_into_list(data_per_algorithm, [-1])
    table_data = create_metrics_table_data(data_per_algorithm_list, 'higher')
    df = create_table(table_data, metric_names)
    return df

def create_dieff_table(id_to_experiment, root_dir, path_to_metric_data, metric_names):
    path = os.path.join(root_dir, path_to_metric_data)
    raw_data = read_raw_metric_data(path)
    raw_data_sorted = dict(sorted(raw_data.items()))
    data_per_algorithm_raw = {id_to_experiment[int(key)]['type']: value for key, value in raw_data_sorted.items()}
    data_per_algorithm = extract_dieff_metrics(data_per_algorithm_raw)
    data_per_algorithm_list = process_metrics_into_list(data_per_algorithm, [None, -1])
    table_data = create_metrics_table_data(data_per_algorithm_list, 'lower')
    df = create_table(table_data, metric_names)
    return df

def to_latex(df):
    print(df.to_latex(multicolumn=True, multirow=True, float_format="%.1f"))

if __name__ == '__main__':
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
    df_r3 = create_r3_table(experiments, ROOT_DIR, os.path.join('data', 'r3-metrics'), ['R3', 'R3Http'])
    df_dieff = create_dieff_table(experiments, ROOT_DIR, os.path.join('data', 'dieff-metrics'), ['Dieff', 'DieffD'])
    # to_latex(df_dieff)
    # mean, std = read_timings_data(experiments, ROOT_DIR)
    mean, std = read_timings_data_single_run(experiments, ROOT_DIR)
    table_data_result_arrival = get_timings_table_data(mean, std)
    df_results = create_table(table_data_result_arrival, ['relRT1st', 'relRTCmpl'])
    joined_df = df_results.join(df_dieff)
    total_df = df_results.join(df_r3).join(df_dieff)
    to_latex(total_df)
    # to_latex(df_dieff)

