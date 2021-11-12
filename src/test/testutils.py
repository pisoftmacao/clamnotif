import os
from clamnotif import config


def full_path(relative_path):
    return os.path.abspath(os.path.join(
        os.path.dirname(__file__), relative_path))


def sample(sample_path):
    return full_path(os.path.join("sample", sample_path))


def sample_cfg():
    return config.load_config(full_path("sample/clamnotif-sample.cfg"))


def remove(path):
    if os.path.isfile(path):
        os.remove(path)


def file_content(report_abspath):
    with open(report_abspath, "r") as f:
        lines = f.readlines()
    return "".join(lines)
