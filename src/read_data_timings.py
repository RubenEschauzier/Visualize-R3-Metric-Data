import math
import os
from collections import defaultdict

import pandas as pd
import numpy as np
from itertools import zip_longest
from fastnumbers import fast_real


def read_query_times(root_dir):
    """
    Reads all `query-times.csv` files in the specified directory structure
    and groups the data by `run_` directories.

    Args:
        root_dir (str): The root directory containing the data structure.

    Returns:
        dict: A dictionary where the keys are `run_` directory names and
              values are pandas DataFrames with the aggregated data from `query-times.csv`.
    """
    run_data = {}

    for root, dirs, files in os.walk(root_dir):
        if 'query-times.csv' in files:
            # Identify the `run_` directory by splitting the root path
            parts = root.split(os.sep)
            run_dir = next((part for part in parts if part.startswith("run_")), None)

            if run_dir:
                # Read the CSV and append it to the corresponding `run_` group
                csv_path = os.path.join(root, 'query-times.csv')
                df = pd.read_csv(csv_path, sep=';')

                if run_dir not in run_data:
                    run_data[run_dir] = []

                run_data[run_dir].append(df)

    output = {}
    for i in range(len(list(run_data.values())[0])):
        output[i] = [query_time[i] for query_time in run_data.values()]
    return output

def rel1st(t_first, t_total, t_first_std, t_total_std):
    rel1st_val = t_first / t_total
    rel1st_var = ((t_first_std / t_first)**2 + (t_total_std / t_total)**2)*(rel1st_val**2)
    return rel1st_val, rel1st_var

def relcmpl(t_last, t_total, t_last_std, t_total_std):
    relcmpl_val = t_last / t_total
    relcmpl_var = ((t_last_std / t_last)**2 + (t_total_std / t_total)**2)*(relcmpl_val**2)
    return relcmpl_val, relcmpl_var

def combine_runs_rel(run_data, experiments_list, timeout):
    experiment_to_rel1st = {}
    experiment_to_relcmpl = {}
    for experiment in experiments_list:
        print(experiment)
        output_key = experiment['combination']
        output_name = experiment['type']
        data = run_data[output_key]
        run_rel1st = defaultdict(list)
        run_rel1st_std = defaultdict(list)
        run_relcmpl = defaultdict(list)
        run_relcmpl_std = defaultdict(list)
        for run in data:
            replications = list(run['replication'])[0]
            grouped_means, grouped_std, grouped_mean_time = group_by_template(run)
            for template in grouped_means.keys():
                template_rel1st = []
                template_rel1st_std = []
                template_relcmpl = []
                template_relcmpl_std = []
                counts = []
                # Iterate over instantiations
                for i in range(len(grouped_means[template])):
                    # For each instantiation we have average timestamps with std and total execution time query
                    # So, we take total execution times, while setting time for queries that time out to timeout value
                    # We take average and std of those execution times, calculate the metrics while using the
                    # propagation of errors formula to get the std of this metric value.
                    times, n_nan_times = convert_to_number(grouped_mean_time[template][i])
                    counts.append(replications)
                    mean_timestamps, _ = convert_to_number(grouped_means[template][i])
                    std_timestamps, _ = convert_to_number(grouped_std[template][i])
                    times = [x if not math.isnan(x) else timeout for x in times]

                    if n_nan_times == len(times) or len(mean_timestamps) == 0:
                        template_rel1st.append(float('nan'))
                        template_rel1st_std.append(float('nan'))
                        template_relcmpl.append(float('nan'))
                        template_relcmpl_std.append(float('nan'))
                        continue

                    rel1st_val, rel1st_std = rel1st(
                        mean_timestamps[0], np.mean(times), std_timestamps[0], np.std(times)
                    )
                    relcmpl_val, relcmpl_std = relcmpl(
                        mean_timestamps[-1], np.mean(times), std_timestamps[-1], np.std(times)
                    )
                    print(relcmpl_val, relcmpl_std)
                    template_rel1st.append(rel1st_val)
                    template_rel1st_std.append(rel1st_std)
                    template_relcmpl.append(relcmpl_val)
                    template_relcmpl_std.append(relcmpl_std)
                # Combine the means of the templates.
                template_mean_rel1st, template_std_rel1st = combine_means_stds_rel(
                    template_rel1st, template_rel1st_std, counts
                )
                template_mean_relcmpl, template_std_relcmpl = combine_means_stds_rel(
                    template_relcmpl, template_relcmpl_std, counts
                )
                run_rel1st[template].append(template_mean_rel1st)
                run_rel1st_std[template].append(math.sqrt(template_std_rel1st))
                run_relcmpl[template].append(template_mean_relcmpl)
                run_relcmpl_std[template].append(math.sqrt(template_std_relcmpl))
        experiment_to_rel1st[output_name] = run_rel1st
        experiment_to_relcmpl[output_name] = run_relcmpl
    return experiment_to_rel1st, experiment_to_relcmpl

def convert_to_number(data):
    as_number = [fast_real(x) for x in data]
    n_nan = len([0 for x in as_number if math.isnan(x)])
    return [fast_real(x) for x in data], n_nan

def combine_runs(run_data, experiments_list):
    combined_outputs_mean = {}
    combined_outputs_std = {}
    for experiment in experiments_list:
        output_key = experiment['combination']
        output_name = experiment['type']
        data = run_data[output_key]
        # {template_0 : [run1: [timestamps_q_0, timestamps_1, run2: [], ...]}
        grouped_runs_mean = {}
        grouped_runs_std = {}
        run_counts = []
        for run in data:
            run_counts.append(list(run['replication'])[0])
            grouped_means, grouped_std, _ = group_by_template(run)
            for key in grouped_means.keys():
                if key not in grouped_runs_mean:
                    grouped_runs_mean[key] = []
                    grouped_runs_std[key] = []
                grouped_runs_mean[key].append(grouped_means[key])
                grouped_runs_std[key].append(grouped_std[key])
        grouped_by_ts_mean = group_by_run_per_timestamp(grouped_runs_mean)
        grouped_by_ts_std = group_by_run_per_timestamp(grouped_runs_std)
        c_mean, c_std = get_combined_means_std(grouped_by_ts_mean, grouped_by_ts_std, run_counts)
        combined_outputs_mean[output_name] = c_mean
        combined_outputs_std[output_name] = c_std
    return combined_outputs_mean, combined_outputs_std


def group_by_template(run_data):
    output_mean = {}
    output_std = {}
    output_times = {}
    grouped_means = run_data.groupby('name')['timestamps'].apply(lambda x: list(x)).to_dict()
    grouped_std = run_data.groupby('name')['timestampsStd'].apply(lambda x: list(x)).to_dict()
    grouped_min = run_data.groupby('name')['timestampsMin'].apply(lambda x: list(x)).to_dict()
    grouped_time = run_data.groupby('name')['times'].apply(lambda x: list(x)).to_dict()

    for key_mean, value_mean in grouped_means.items():
        # For short-1 we use the minimal timestamps, as this run went wrong and the averaged are ruined
        # By a single excessively long-running query (timestamp > query run time).
        if key_mean == 'interactive-short-1':
            output_mean[key_mean] = [timestamps.split(' ') if isinstance(timestamps, str) else []
                                     for timestamps in grouped_min[key_mean]]
        else:
            output_mean[key_mean] = [timestamps.split(' ') if isinstance(timestamps, str) else []
                                     for timestamps in value_mean]
    for key_std, value_std in grouped_std.items():
        output_std[key_std] = [timestamps.split(' ') if isinstance(timestamps, str) else []
                               for timestamps in value_std]
    for key_times, value_times in grouped_time.items():
        output_times[key_times] = [timestamps.split(' ') if isinstance(timestamps, str) else []
                               for timestamps in value_times]

    return output_mean, output_std, output_times


def group_by_run_per_timestamp(data):
    # Output will be: {template: [ instantiation [ [f_ts_0, fs_ts_1, ...], [sec_ts_0, sec_ts_1], ... ] ], ...}
    output = {}
    for (template, value) in data.items():
        run_agg = []
        # First iterate over all query instantiations
        for i in range(len(value[0])):
            lists_to_merge = []
            for run in range(len(value)):
                lists_to_merge.append(value[run][i])

            merged = [list(x) for x in list(zip_longest(*lists_to_merge, fillvalue=None))]
            run_agg.append(merged)
        output[template] = run_agg
    return output


def get_combined_means_std(grouped_by_ts_mean, grouped_by_ts_std, run_counts):
    output_mean = {}
    output_std = {}
    for key in grouped_by_ts_mean.keys():
        means_template = grouped_by_ts_mean[key]
        stds_template = grouped_by_ts_std[key]
        template_output_mean = []
        template_output_std = []
        for inst in range(len(means_template)):
            ts_instantiation_mean = []
            ts_instantiation_std = []
            for ts in range(len(means_template[inst])):
                # First remove any Nones, which indicate that only one run had an entry for that timestamp
                # Then convert to a number
                means = [fast_real(x) for x in [y for y in means_template[inst][ts] if y is not None]]
                stds = [fast_real(x) for x in [y for y in stds_template[inst][ts] if y is not None]]
                c_mean, c_std = combine_means_stds(means, stds, run_counts)
                ts_instantiation_mean.append(c_mean)
                ts_instantiation_std.append(c_std)
            template_output_mean.append(ts_instantiation_mean)
            template_output_std.append(ts_instantiation_std)
        output_mean[key] = template_output_mean
        output_std[key] = template_output_std
    return output_mean, output_std


# From https://www.statstodo.com/CombineMeansSDs.php
def combine_means_stds(means, std, counts):
    ex = []
    exx = []
    tn = 0
    tx = 0
    txx = 0
    for i in range(len(means)):
        ex.append(counts[i] * means[i])
        exx.append(std[i] ** 2 * (counts[i] - 1) + (ex[i] ** 2 / counts[i]))
        tn += counts[i]
        tx += ex[i]
        txx += exx[i]
    combined_mean = tx / tn
    combined_var = (txx - (tx ** 2 / tn)) / (tn - 1)
    combined_std = math.sqrt(combined_var)
    return combined_mean, combined_std


def combine_means_stds_rel(means, std, counts):
    nans = np.isnan(means)
    print(means)
    means = np.array(means)[~nans]
    std = np.array(std)[~nans]
    counts = np.array(counts)[~nans]
    if len(means) == 0:
        return float('nan'), float('nan')
    ex = []
    exx = []
    tn = 0
    tx = 0
    txx = 0
    for i in range(len(means)):
        ex.append(counts[i] * means[i])
        exx.append(std[i] ** 2 * (counts[i] - 1) + (ex[i] ** 2 / counts[i]))
        tn += counts[i]
        tx += ex[i]
        txx += exx[i]
    combined_mean = tx / tn
    combined_var = (txx - (tx ** 2 / tn)) / (tn - 1)
    combined_std = math.sqrt(combined_var)
    return combined_mean, combined_std

def average_time_first_last_result(combined_runs):
    output = {}
    for (experiment, templates) in combined_runs.items():
        experiment_output = {}
        for (template, timestamps_inst) in templates.items():
            n = 0
            tfr = 0
            tlr = 0
            for timestamps in timestamps_inst:
                if len(timestamps) > 0:
                    tfr += timestamps[0]
                    tlr += timestamps[-1]
                    n += 1
            if n > 0:
                mean_tfr = tfr / n
                mean_tlr = tlr / n
            else:
                mean_tlr = -1
                mean_tfr = -1
            experiment_output[template] = [mean_tfr, mean_tlr]
        output[experiment] = experiment_output
    return output


def make_relative(data):
    output = {}
    for experiment, templates in data.items():
        relative_to_bfs = {}
        for template, timestamps in data[experiment].items():
            if timestamps[1] == 0:
                relative_to_bfs[template] = [-1, -1]
            else:
                relative_to_bfs[template] = [x / data['breadth-first'][template][1] for x in timestamps]
                # relative_to_bfs[template] = [ex/base for ex, base in zip(timestamps, data['breadth-first'][template])]
        output[experiment] = relative_to_bfs

    return output


def prepare_plot_data(data):
    # Convert plot data from experiment : template : timings to template : [ timings_first ] [timings_last] [experiment]
    template_to_data = {}
    experiments = data.keys()
    for template, timings in list(data.values())[0].items():
        experiment_timings_first = []
        experiment_timings_last = []
        for experiment in experiments:
            experiment_timings_first.append(data[experiment][template][0])
            experiment_timings_last.append(data[experiment][template][1])
        template_to_data[template] = [experiment_timings_first, experiment_timings_last, experiments]
    return template_to_data

def prepare_plot_data_corrected(data_rel1st, data_relcmpl):
    template_to_data = {}
    experiments = data_rel1st.keys()
    for template, timings in list(data_rel1st.values())[0].items():
        experiment_timings_rel1st = []
        experiment_timings_relcmpl = []
        for experiment in experiments:
            mean_of_runs_rel1st = np.mean(data_rel1st[experiment][template])
            mean_of_runs_relcmpl = np.mean(data_relcmpl[experiment][template])
            experiment_timings_rel1st.append(mean_of_runs_rel1st)
            experiment_timings_relcmpl.append(mean_of_runs_relcmpl)

        template_to_data[template] = [experiment_timings_rel1st, experiment_timings_relcmpl, experiments]
    return template_to_data

def prepare_single_run(data, experiments, run_id):
    template_data = {}
    run_data = data[run_id]
    for experiment in experiments:
        output_key = experiment['combination']
        output_name = experiment['type']
        single_run = data[output_key][run_id]
        templates = list(set(single_run['name']))
        templates.sort()

        for template in templates:
            template_timings = single_run.loc[single_run['name'] == template]
            instantiation_timestamps = list(template_timings['timestamps'])
            for timestamps_string in instantiation_timestamps:
                if isinstance(timestamps_string, str):
                    timestamps_list = [ fast_real(timestamp) for timestamp in timestamps_string.split(' ')]


        timestamps_string = single_run['timestamps']

    pass


if __name__ == "__main__":
    pass
    # experiments = [
    #     {"type": "breadth-first", "combination": 0},
    #     {"type": "depth-first", "combination": 1},
    #     {"type": "random", "combination": 2},
    #     {"type": "in-degree", "combination": 3},
    #     {"type": "pagerank", "combination": 4},
    #     {"type": "rcc-1", "combination": 5},
    #     {"type": "rcc-2", "combination": 6},
    #     {"type": "rel-1", "combination": 7},
    #     {"type": "rel-2", "combination": 8},
    #     {"type": "is", "combination": 9},
    #     {"type": "isdcr", "combination": 10},
    #     {"type": "is-rcc-1", "combination": 11},
    #     {"type": "is-rcc-2", "combination": 12},
    #     {"type": "is-rel-1", "combination": 13},
    #     {"type": "is-rel-2", "combination": 14}
    # ]
    # timings = read_query_times(os.path.join(ROOT_DIR, 'data'))
    # combine_means_stds([2, 4, 6, 2, 3], [5, 9, 3, 5, 10], [1.2, 2.3, 4.5, 3, 2])
    # combined_mean, combined_std = combine_runs(timings, experiments)
    # result = average_time_first_last_result(combined_mean)
    # relative = make_relative(result)
