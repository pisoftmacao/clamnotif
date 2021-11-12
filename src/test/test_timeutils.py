import unittest

from clamnotif import timeutils
import datetime


class TimeUtilsTestCase(unittest.TestCase):

    def testNowDiffLessThenOneSecond(self):
        now = timeutils.time2str(datetime.datetime.now())
        now2 = timeutils.time2str(timeutils.now())
        self.assertEqual(now, now2)
