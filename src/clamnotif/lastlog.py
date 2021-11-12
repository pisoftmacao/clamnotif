import json
import os
from datetime import datetime
from .default import default_values
from .timeutils import timeutils


def _parse_datetime(_dict):
    for k, v in _dict.items():
        if isinstance(v, str) and k in ["report_start_time", "heartbeat_time"]:
            try:
                _dict[k] = timeutils.str2time(v)
            except:
                _dict[k] = None
                pass
    return _dict


def _convert_datetime(o):
    if isinstance(o, datetime):
        return timeutils.time2str(o)


class LastLog(object):
    def __init__(self, _default_values):
        self.default_values = _default_values

    def get(self):
        lastlog_path = self.default_values.lastlog_path()
        if not os.path.isfile(lastlog_path):
            return {"report_start_time": None,
                    "heartbeat_time": None,
                    "lastlog_path": lastlog_path}
        with open(lastlog_path, "r") as f:
            log_entry = json.load(f, object_hook=_parse_datetime)
            log_entry["lastlog_path"] = lastlog_path
            return log_entry

    def persist(self, log_entry):
        with open(log_entry["lastlog_path"], "w") as f:
            json.dump(log_entry, f, default=_convert_datetime)


lastlog = LastLog(default_values)
