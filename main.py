# import numpy as np
# import pandas as pd
import os
#
# from src.create_better_worse_tables import get_timings_table_data, create_table
# from src.create_plots import create_comparative_bar_plot, create_plots_dieff, create_big_comparative_bar_plot
# from src.read_data_dieff import read_raw_metric_data
# from src.read_data_timings import read_query_times, combine_means_stds, combine_runs, average_time_first_last_result, \
#     make_relative, prepare_plot_data
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
#
# def create_combined_timings_plot(id_to_experiment, root_dir):
#     timings = read_query_times(os.path.join(root_dir, 'data'))
#     combined_mean, combined_std = combine_runs(timings, id_to_experiment)
#     result = average_time_first_last_result(combined_mean)
#     relative = make_relative(result)
#     plot_data = prepare_plot_data(relative)
#     save_location_plot = os.path.join(root_dir, 'output', 'timing_plots', 'combined_timing_plot.pdf')
#     create_big_comparative_bar_plot(plot_data, save_location_plot)
#
#
#
# if __name__ == "__main__":
#     experiments = [
#         {"type": "breadth-first", "combination": 0},
#         {"type": "depth-first", "combination": 1},
#         {"type": "random", "combination": 2},
#         {"type": "in-degree", "combination": 3},
#         {"type": "pagerank", "combination": 4},
#         {"type": "rcc-1", "combination": 5},
#         {"type": "rcc-2", "combination": 6},
#         {"type": "rel-1", "combination": 7},
#         {"type": "rel-2", "combination": 8},
#         {"type": "is", "combination": 9},
#         {"type": "isdcr", "combination": 10},
#         {"type": "is-rcc-1", "combination": 11},
#         {"type": "is-rcc-2", "combination": 12},
#         {"type": "is-rel-1", "combination": 13},
#         {"type": "is-rel-2", "combination": 14}
#     ]
#     # create_combined_timings_plot(experiments, ROOT_DIR)
#     table_data_result_arrival = get_timings_table_data(experiments, ROOT_DIR)
#     df_results = create_table(table_data_result_arrival, ['relRT1st', 'relRTCmpl'])
#     print(df_results.to_latex(multicolumn = True, multirow = True, float_format="%.2f"))
#     # for template, timings in plot_data.items():
#     #     save_location_plot = os.path.join(ROOT_DIR, 'output', 'timing_plots', '{}.pdf'.format(template))
#     #     create_comparative_bar_plot(timings[2], timings[0], timings[1],
#     #                                 title=template, save_location=save_location_plot)
#     # data_dieff = read_raw_dieff_data(os.path.join(ROOT_DIR, 'data', 'dieff_data'))
#     # create_plots_dieff(data_dieff)
#     # import matplotlib.pyplot as plt
#     # import numpy as np
#     #
