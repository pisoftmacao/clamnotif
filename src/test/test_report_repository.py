import logging
import os

import unittest


from clamnotif import report_repository
from datetime import datetime
from .testutils import *


def clamav_report_folder(case_name):
    return full_path(
        "sample/clamav_report/" + case_name)


class HealthReportRepositoryTestCase(unittest.TestCase):

    def testLookupLatestReportClamAVReportsOnly(self):
        folder = clamav_report_folder("clamav_only")
        report = report_repository.find_last_report(folder)
        self.assertIsNotNone(report)
        self.assertEqual(0, report.infected_number)
        start_time = datetime.strptime(
            '2021:11:03 13:30:38', '%Y:%m:%d %H:%M:%S')
        self.assertEqual(start_time,  report.start_time)
        self.assertEqual(file_content(
            os.path.join(folder, "clamav-report-later.log")), report.content)

    def testLookupLatestReportEmptyFolder(self):
        folder = clamav_report_folder("empty")
        report = report_repository.find_last_report(folder)
        self.assertIsNone(report)

    def testLookupLatestReportMixedWithNonClamAVFiles(self):
        folder = clamav_report_folder("mixed")
        report = report_repository.find_last_report(folder)
        self.assertIsNotNone(report)
        self.assertEqual(0, report.infected_number)
        start_time = datetime.strptime(
            '2021:11:03 13:30:38', '%Y:%m:%d %H:%M:%S')
        self.assertEqual(start_time,  report.start_time)
        self.assertEqual(file_content(
            os.path.join(folder, "clamav-report-later.log")), report.content)

    def testLookupLatestReportNonClamAVFilesOnly(self):
        folder = clamav_report_folder("non_clamav_only")
        report = report_repository.find_last_report(folder)
        self.assertIsNone(report)
