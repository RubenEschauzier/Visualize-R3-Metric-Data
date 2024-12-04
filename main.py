import numpy as np
import pandas
import os

from src.create_plots import create_comparative_bar_plot
from src.read_data import read_query_times, combine_means_stds, combine_runs, average_time_first_last_result, \
    make_relative, prepare_plot_data

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

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
    timings = read_query_times(os.path.join(ROOT_DIR, 'data'))
    combined_mean, combined_std = combine_runs(timings, experiments)
    result = average_time_first_last_result(combined_mean)
    relative = make_relative(result)
    plot_data = prepare_plot_data(relative)

    for template, timings in plot_data.items():
        create_comparative_bar_plot(timings[2], timings[0], timings[1], title="TEST")
