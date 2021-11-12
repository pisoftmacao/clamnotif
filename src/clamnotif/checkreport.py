import logging
import os

from .clamreport import clamreport
from .lastlog import lastlog
from .messenger import messenger
from .timeutils import timeutils


class CheckReport(object):
    def __init__(self, _messenger, _clamreport, _lastlog, _timeutils):
        self.messenger = _messenger
        self.clamreport = _clamreport
        self.lastlog = _lastlog
        self.timeutils = _timeutils

    def _send_heartbeat(self, mail_content, cfg, report):
        now = self.timeutils.now()
        last = self.lastlog.get()
        last_heartbeat_time = last["heartbeat_time"]
        if last_heartbeat_time is None\
                or (now - last_heartbeat_time).days >= cfg.heartbeat_day_gap:
            self.messenger.send_heartbeat(mail_content, cfg)
            last["heartbeat_time"] = now
            if report is not None:
                last["report_start_time"] = report.start_time
            self.lastlog.persist(last)
        else:
            more_days = cfg.heartbeat_day_gap - \
                (now - last_heartbeat_time).days
            logging.info(
                "no heartbeat send. should wait for {} more day(s).".format(more_days))

    def process(self, cfg):
        report_folder = os.path.expanduser(cfg.clamav_report_folder)
        logging.info("looking up reports from {} ...".format(report_folder))
        report = self.clamreport.find_last_report(report_folder)
        if report == None:
            mail_content = "Please be noticed that there are no report found in {}".format(
                cfg.clamav_report_folder)
            logging.info(
                "no report found. Try sending a reminder heartbeat...")
            self._send_heartbeat(mail_content, cfg, report)
            logging.info("done.")
        elif report.infected_number == 0:
            logging.info(
                "no files infected. Try sending a heartbeat...")
            self._send_heartbeat(report.content, cfg, report)
            logging.info("done.")
        else:
            logging.info(
                "{} files infected. Try sending an alert...".format(report.infected_number))
            self.messenger.send_alert(report.content, cfg)
            logging.info("done.")


checkreport = CheckReport(messenger, clamreport, lastlog, timeutils)
