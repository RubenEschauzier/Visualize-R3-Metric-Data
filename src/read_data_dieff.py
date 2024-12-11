import math
import os
import json
import pandas as pd
import numpy as np
import re


def read_raw_metric_data(data_path):
    experiment_to_data = {}
    for filename in os.listdir(data_path):
        with open(os.path.join(data_path, filename)) as f:
            data = json.load(f)
            match = re.search(r'_(\d+)\.json$', filename)
            experiment_to_data[int(match.group(1))] = data
    return experiment_to_data


if __name__ == "__main__":
    pass