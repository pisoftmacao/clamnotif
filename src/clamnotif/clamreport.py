import logging
import os

from datetime import datetime
from .reportreader import reportreader


class HealthReportRepository(object):

    def find_last_report(self, report_folder):
        files = os.listdir(report_folder)
        if len(files) == 0:
            return None
        files = [os.path.join(report_folder, f) for f in files]
        reports = [reportreader.read(f) for f in files]
        reports = [r for r in reports if r.start_time is not None]
        reports = sorted(reports, key=lambda x: x.start_time, reverse=True)
        if len(reports) == 0:
            return None
        return reports[0]


clamreport = HealthReportRepository()
