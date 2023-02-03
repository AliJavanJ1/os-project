import importlib
import re
import numpy as np
from sklearn.model_selection import train_test_split

from app.models import Run


def train_scikit_learn(run_id):
    """
    train scikit learn model
    :param run_id:
    :return:
    """
    print("train_scikit_learn")
    run = Run.objects.get(id=run_id)
    # load data
    data = np.load(run.project.data_file.path)
    target_data = np.load(run.project.target_data_file.path)
    # split data
    x_train, x_test, y_train, y_test = train_test_split(data, target_data, test_size=run.split_ratio)
    # load model
    path = re.sub(r"\.py$", "", run.project.model.code_file.url).replace("/", ".")
    model = importlib.import_module(path[1:]).model
    # train model
    model.fit(x_train, y_train)
    # test model
    result = model.score(x_test, y_test)
    # save result
    print("result: ", result, "\nmodel: ", model)


def train_tensorflow(run_id):
    pass


def train_pytorch(run_id):
    pass


def train_opencv(run_id):
    pass


def hook_after_train(task):  # use for error handling
    print(task.time_taken(), task.success, task.result)
