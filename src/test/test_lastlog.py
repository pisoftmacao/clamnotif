import json
import unittest

from datetime import datetime

from clamnotif import default_values, lastlog, timeutils

from .testutils import *


class MockDefaultValues(object):

    def __init__(self):
        self.trace = ""

    def lastlog_path(self):
        self.trace = self.trace + "l"
        return sample("lastlog.json")


class MockNotExistValues(object):

    def __init__(self):
        self.trace = ""

    def lastlog_path(self):
        self.trace = self.trace + "l"
        return sample("not-exist.json")


class MockNewLastLogValues(object):

    def __init__(self):
        self.trace = ""

    def lastlog_path(self):
        self.trace = self.trace + "l"
        return sample("lastlog-new.json")


class MockNullValues(object):

    def __init__(self):
        self.trace = ""

    def lastlog_path(self):
        self.trace = self.trace + "l"
        return sample("lastlog-null.json")


class LastLogTestCase(unittest.TestCase):

    def testLastLogInitialisation(self):
        self.assertEqual(lastlog.default_values, default_values)

    def testGetWhenLastLogExist(self):
        lastlog.default_values = MockDefaultValues()
        last = lastlog.get()
        self.assertEqual("l", lastlog.default_values.trace)
        self.assertEqual(sample("lastlog.json"), last["lastlog_path"])
        self.assertEqual("2021-11-03 22:15:00",
                         timeutils.time2str(last["report_start_time"]))
        self.assertEqual("2021-11-04 03:15:00",
                         timeutils.time2str(last["heartbeat_time"]))
        lastlog.default_values = default_values

    def testGetWhenLastLogNotExist(self):
        lastlog.default_values = MockNotExistValues()
        last = lastlog.get()
        self.assertEqual("l", lastlog.default_values.trace)
        self.assertIsNone(last["report_start_time"])
        self.assertIsNone(last["heartbeat_time"])
        self.assertEqual(sample("not-exist.json"), last["lastlog_path"])
        lastlog.default_values = default_values

    def testGetLastLogHavingNullValues(self):
        lastlog.default_values = MockNullValues()
        last = lastlog.get()
        self.assertEqual("l", lastlog.default_values.trace)
        self.assertIsNone(last["report_start_time"])
        self.assertEqual("2021-11-04 03:15:00",
                         timeutils.time2str(last["heartbeat_time"]))
        self.assertEqual(sample("lastlog-null.json"), last["lastlog_path"])
        lastlog.default_values = default_values

    def testPersistLastLog(self):
        lastlog.default_values = MockNewLastLogValues()
        lastlog_path = sample("lastlog-new.json")
        remove(lastlog_path)
        # case 01: lastlog-new does not exist
        last = lastlog.get()
        self.assertIsNone(last["report_start_time"])
        self.assertIsNone(last["heartbeat_time"])
        self.assertEqual(lastlog_path, last["lastlog_path"])
        self.assertFalse(os.path.isfile(lastlog_path))
        # case 02: persist field report_start_time
        last["report_start_time"] = timeutils.str2time("2021-11-10 11:02:30")
        lastlog.persist(last)
        last2 = lastlog.get()
        self.assertIsNone(last2["heartbeat_time"])
        self.assertEqual(last["report_start_time"], last2["report_start_time"])
        self.assertTrue(os.path.isfile(lastlog_path))
        # case 03: persist field heartbeat_time
        last2["heartbeat_time"] = timeutils.str2time("2021-11-15 11:02:30")
        lastlog.persist(last2)
        last3 = lastlog.get()
        self.assertEqual(last["report_start_time"], last3["report_start_time"])
        self.assertEqual(last2["heartbeat_time"],
                         last3["heartbeat_time"])
        lastlog.default_values = default_values
        remove(lastlog_path)
