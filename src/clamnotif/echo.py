import os

from .terminal import terminal
from .default import default_values


class Echo(object):

    def welcome(self):
        verison_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), '_version.txt')
        with open(verison_file, 'r', encoding="utf-8") as f:
            version_num = f.readline().strip()
        terminal.welcome(
            "Welcome for using ClamNotif v{} brought to you by PiSoft Company Ltd.".format(version_num))

    def checkcfg_file_exist_start(self):
        terminal.header("Checking for ~/.clamnotif/clamnotif.cfg ...")

    def checkcfg_file_exist_success(self):
        terminal.checked("{} found".format(default_values.cfg_path()))

    def checkcfg_file_exist_failed(self):
        terminal.unchecked("{} not found".format(default_values.cfg_path()))

    def checkcfg_file_exist_failed_tips(self):
        terminal.please_run("python3 -m clamnotif --create-cfg",
                            "create a sample configuration")

    def testsmtp_start(self):
        terminal.header("Verifying SMTP Settings...")

    def testsmtp_success(self, cfg):
        terminal.success(
            "Successfully sent a testing email with title 'ClamNotif Testing' to {} and {}.".format(
                cfg.heartbeat_receiver_addresses,
                cfg.alert_receiver_addresses))


echo = Echo()
