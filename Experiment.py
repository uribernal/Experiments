import os
import json
import datetime
import xlsxwriter
import time
import numpy as np


def get_experiments():
    path = 'experiments.json'
    if os.path.isfile(path):
        with open(path) as data_file:
            data = json.load(data_file)
    else:
        data = {}

    return data


def get_actual_experiment_id():
    experiments = get_experiments()
    return len(experiments.keys())


def get_elapsed_time(elapsed):
    hours = 0
    minutes = 0
    if elapsed / 3600 >= 1:
        hours = int(elapsed / 3600)
        minutes = int((elapsed % 3600) / 60)
    elif elapsed / 60 >= 1:
        minutes = int(elapsed / 60)
    return '{0:02d}h{1:02d}min'.format(hours, minutes)


class Experiment:
    'Common base class for all Experiments'
    json_path = 'experiments.json'
    xls_path = 'experiments.xls'
    experiment_id = None
    date = None
    start = None
    elapsed = None
    param1 = None
    param2 = None
    param3 = None
    result1 = None
    result2 = None

    def __init__(self, param1, param2, param3):
        # Get last experiment
        Experiment.experiment_id = get_actual_experiment_id()

        # Compute date
        Experiment.date = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")

        Experiment.start = time.time()

        Experiment.param1 = param1
        Experiment.param2 = param2
        Experiment.param3 = param3

    def save_results(self, result1, result2):
        Experiment.elapsed = get_elapsed_time(time.time() - Experiment.start )
        Experiment.result1 = result1
        Experiment.result2 = result2

        # Save Experiment
        Experiment.save_json(self)
        Experiment.save_xls(self)

    def save_json(self):
        # Get experiments
        experiments = get_experiments()

        # Update experiments
        experiments[str(Experiment.experiment_id)] = {
            'date': Experiment.date,
            'elapsed': Experiment.elapsed,
            'param1': Experiment.param1,
            'param2': Experiment.param2,
            'param3': Experiment.param3,
            'result1': Experiment.result1,
            'result2': Experiment.result2}

        # Update JSON
        s = json.dumps(experiments)
        with open(self.json_path, 'w') as f:
            f.write(s)

    def save_xls(self):
        items = ['date', 'elapsed', 'param1', 'param2', 'param3', 'result1', 'result2']
        keys = np.arange(get_actual_experiment_id())
        # Get experiments
        experiments = get_experiments()

        # Update XLS
        workbook = xlsxwriter.Workbook(self.xls_path)
        worksheet = workbook.add_worksheet()
        worksheet.write(0, 0, 'experiment_id')

        col = 0
        for key in keys:
            key = str(key)
            row = 0
            worksheet.write(col + 1, row, key)
            for item in items:
                # If never created, first col with names
                if col == 0:
                    worksheet.write(col, row + 1, item)
                # Write experiment
                worksheet.write(col + 1, row + 1, experiments[key][item])
                row += 1
            col += 1

        workbook.close()

e = Experiment(1, 2, 3)
e.save_results(10, 20)
e = Experiment(4, 5, 6)
e.save_results(40, 50)
e = Experiment(7, 8, 9)
time.sleep(5)
e.save_results(70, 80)
print(e.experiment_id)
