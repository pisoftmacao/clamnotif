import logging

from datetime import datetime


class HealthReport(object):
    def __init__(self, infected_number, start_time, content):
        self.infected_number = infected_number
        self.start_time = start_time
        self.content = content


STR_INFECTED_FILES = "Infected files:"
STR_START_DATE = "Start Date:"
STR_CLAMAV_DATE_FMT = "%Y:%m:%d %H:%M:%S"


class HealthReportReader(object):

    def read(self, report_abspath):
        report = HealthReport(None, None, None)
        with open(report_abspath, "r") as f:
            lines = f.readlines()
        report.content = "".join(lines)
        for line in lines:
            if line.startswith(STR_INFECTED_FILES):
                report.infected_number = int(
                    line.replace(STR_INFECTED_FILES, "").strip())
            if line.startswith(STR_START_DATE):
                start_time_str = line.replace(STR_START_DATE, "").strip()
                report.start_time = datetime.strptime(
                    start_time_str, STR_CLAMAV_DATE_FMT)
            if report.infected_number is not None and report.start_time is not None:
                return report
        return report


reportreader = HealthReportReader()
