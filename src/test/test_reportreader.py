import logging
import unittest

from clamnotif import reportreader as reader
from datetime import datetime
from .testutils import *


class ReportReaderTestCase(unittest.TestCase):

    def testReadHeartbeatReport(self):
        report_abspath = full_path(
            "sample/clamav-report-heartbeat.log")
        report = reader.read(report_abspath)
        self.assertIsNotNone(report)
        self.assertEqual(0, report.infected_number)
        start_time = datetime.strptime(
            '2021:11:03 13:30:38', '%Y:%m:%d %H:%M:%S')
        self.assertEqual(start_time,  report.start_time)
        self.assertEqual(file_content(
            report_abspath), report.content)

    def testReadAlertReport(self):
        report_abspath = full_path(
            "sample/clamav-report-alert.log")
        report = reader.read(report_abspath)
        self.assertIsNotNone(report)
        self.assertEqual(9, report.infected_number)
        start_time = datetime.strptime(
            '2021:11:03 14:30:38', '%Y:%m:%d %H:%M:%S')
        self.assertEqual(start_time,  report.start_time)
        self.assertEqual(file_content(
            report_abspath), report.content)

    def testReadNonClamAVReport(self):
        report_abspath = full_path(
            "sample/clamnotif-sample.cfg")
        report = reader.read(report_abspath)
        self.assertIsNotNone(report)
        self.assertIsNone(report.start_time)
        self.assertIsNone(report.infected_number)
        self.assertEqual(file_content(
            report_abspath), report.content)
