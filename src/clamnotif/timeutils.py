import datetime
from datetime import datetime as dt


class TimeUtils(object):

    def __init__(self):
        self._default_time_fmt = "%Y-%m-%d %H:%M:%S"

    def str2time(self, timestr):
        return dt.strptime(timestr, self._default_time_fmt)

    def time2str(self, time):
        return time.strftime(self._default_time_fmt)

    def now(self):
        return datetime.datetime.now()


timeutils = TimeUtils()
