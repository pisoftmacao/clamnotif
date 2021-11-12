import unittest

import os

from datetime import datetime

from clamnotif import clamreport, config, messenger, checkreport, lastlog, timeutils
from clamnotif.reportreader import HealthReport
from .testutils import *


class HeartbeatClamReport(object):
    def __init__(self, start_time):
        self.trace = ""
        self.start_time = start_time

    def find_last_report(self, report_folder):
        self.trace = "f"
        self.report_folder = report_folder
        return HealthReport(0, self.start_time, "Heartbeat")


class MockTimeUtils(object):
    def __init__(self, _now):
        self.trace = ""
        self._now = _now

    def now(self):
        self.trace = self.trace + "n"
        return self._now


class AlertClamReport(object):
    def __init__(self):
        self.trace = ""

    def find_last_report(self, report_folder):
        self.trace = "f"
        self.report_folder = report_folder
        start_time = datetime.strptime(
            '2021:11:03 13:30:38', '%Y:%m:%d %H:%M:%S')
        return HealthReport(10, start_time, "Alert!!!")


class NoneClamReport(object):
    def __init__(self):
        self.trace = ""

    def find_last_report(self, report_folder):
        self.trace = "f"
        self.report_folder = report_folder
        return None


class MockMessenger(object):
    def __init__(self):
        self.trace = ""

    def send_heartbeat(self, mail_content, config):
        self.trace = self.trace + "h"
        self.mail_content = mail_content
        self.config = config

    def send_alert(self, mail_content, config):
        self.trace = self.trace + "a"
        self.mail_content = mail_content
        self.config = config


class MockLastLog(object):
    def __init__(self, heartbeat_time):
        self.heartbeat_time = heartbeat_time
        self.trace = ""

    def get(self):
        self.trace = self.trace + "g"
        return {
            "heartbeat_time": self.heartbeat_time,
            "report_start_time": None
        }

    def persist(self, log):
        self.trace = self.trace + "_p"
        self.persist_heartbeat_time = log["heartbeat_time"]
        self.persist_report_start_time = log["report_start_time"]


class CheckReportTestCase(unittest.TestCase):

    def testCheckReportInitialisation(self):
        self.assertEqual(checkreport.messenger, messenger)
        self.assertEqual(checkreport.clamreport, clamreport)
        self.assertEqual(checkreport.lastlog, lastlog)
        self.assertEqual(checkreport.timeutils, timeutils)

    def testSendHeartbeat(self):
        c = config.load_config(
            full_path("sample/clamnotif-sample.cfg"))
        self.assertEqual(2, c.heartbeat_day_gap)
        # case 01:(now - heartbeat_time).days >= cfg.heartbeat_day_gap
        checkreport.messenger = MockMessenger()
        checkreport.clamreport = HeartbeatClamReport(
            timeutils.str2time('2021-11-03 13:30:38'))
        checkreport.timeutils = MockTimeUtils(
            timeutils.str2time('2021-11-04 03:15:00'))
        checkreport.lastlog = MockLastLog(
            heartbeat_time=timeutils.str2time('2021-11-02 03:15:00'))
        checkreport.process(c)
        self.assertEqual("f", checkreport.clamreport.trace)
        self.assertEqual(os.path.expanduser(
            c.clamav_report_folder), checkreport.clamreport.report_folder)
        self.assertEqual("h", checkreport.messenger.trace)
        self.assertEqual(c, checkreport.messenger.config)
        self.assertEqual("Heartbeat", checkreport.messenger.mail_content)
        self.assertEqual("n", checkreport.timeutils.trace)
        self.assertEqual("g_p", checkreport.lastlog.trace)
        self.assertEqual(checkreport.timeutils.now(),
                         checkreport.lastlog.persist_heartbeat_time)
        self.assertEqual(timeutils.str2time('2021-11-03 13:30:38'),
                         checkreport.lastlog.persist_report_start_time)
        # case 02:(now - heartbeat_time).days < cfg.heartbeat_day_gap
        checkreport.timeutils = MockTimeUtils(
            _now=timeutils.str2time('2021-11-03 03:15:00'))
        checkreport.process(c)
        self.assertEqual("h", checkreport.messenger.trace)
        self.assertEqual("g_pg", checkreport.lastlog.trace)
        # case 03: heartbeat_time is None
        checkreport.lastlog = MockLastLog(heartbeat_time=None)
        checkreport.process(c)
        self.assertEqual("hh", checkreport.messenger.trace)
        self.assertEqual("g_p", checkreport.lastlog.trace)
        self.assertEqual(checkreport.timeutils.now(),
                         checkreport.lastlog.persist_heartbeat_time)
        checkreport.messenger = messenger
        checkreport.clamreport = clamreport
        checkreport.timeutils = timeutils
        checkreport.lastlog = lastlog

    def testSendAlert(self):
        c = config.load_config(
            full_path("sample/clamnotif-sample.cfg"))
        checkreport.messenger = MockMessenger()
        checkreport.clamreport = AlertClamReport()
        # make sure no call to lastlog and timeutils if we are sending an alert
        checkreport.lastlog = None
        checkreport.timeutils = None
        checkreport.process(c)
        self.assertEqual("f", checkreport.clamreport.trace)
        self.assertEqual(os.path.expanduser(
            c.clamav_report_folder), checkreport.clamreport.report_folder)
        self.assertEqual("a", checkreport.messenger.trace)
        self.assertEqual(c, checkreport.messenger.config)
        self.assertEqual("Alert!!!", checkreport.messenger.mail_content)
        checkreport.messenger = messenger
        checkreport.clamreport = clamreport

    def testSendNoReportFound(self):
        c = config.load_config(
            full_path("sample/clamnotif-sample.cfg"))
        checkreport.messenger = MockMessenger()
        checkreport.clamreport = NoneClamReport()
        checkreport.timeutils = MockTimeUtils(
            timeutils.str2time('2021-11-04 03:15:00'))
        checkreport.lastlog = MockLastLog(
            heartbeat_time=timeutils.str2time('2021-11-02 03:15:00'))

        checkreport.process(c)
        self.assertEqual("f", checkreport.clamreport.trace)
        self.assertEqual(os.path.expanduser(
            c.clamav_report_folder), checkreport.clamreport.report_folder)
        self.assertEqual("h", checkreport.messenger.trace)
        self.assertEqual(c, checkreport.messenger.config)
        self.assertEqual("Please be noticed that there are no report found in ~/.ClamAV/daily/",
                         checkreport.messenger.mail_content)
        self.assertEqual("n", checkreport.timeutils.trace)
        self.assertEqual("g_p", checkreport.lastlog.trace)
        self.assertEqual(checkreport.timeutils.now(),
                         checkreport.lastlog.persist_heartbeat_time)
        self.assertIsNone(checkreport.lastlog.persist_report_start_time)
        checkreport.messenger = messenger
        checkreport.clamreport = clamreport
        checkreport.timeutils = timeutils
        checkreport.lastlog = lastlog
