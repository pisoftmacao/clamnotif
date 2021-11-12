import configparser
import os

from .default import default_values


class ClamNotifConfig(object):
    def __init__(self, config):
        self.smtp_server_host = config['SMTP']['SMTPServerHost']
        self.smtp_server_port = config['SMTP'].getint('SMTPServerPort')
        self.smtp_tls_enabled = config['SMTP'].getboolean('SMTPTLSEnabled')
        self.sender_address = config['Notification']['SenderAddress']
        self.sender_passwd = config['Notification']['SenderPasswd']
        self.alert_subject = config['Notification']['AlertSubject']
        self.alert_receiver_addresses = config['Notification']['AlertReceiverAddresses']
        self.heartbeat_subject = config['Notification']['HeartbeatSubject']
        self.heartbeat_receiver_addresses = config['Notification']['HeartbeatReceiverAddresses']
        self.heartbeat_day_gap = config['Notification'].getint(
            'HeartbeatDayGap')
        self.clamav_report_folder = config['ClamAV']['ClamAVReportFolder']


class ClamNotifConfigLoader(object):

    def load_config(self, path):
        c = configparser.ConfigParser()
        c.read(path)
        return ClamNotifConfig(c)

    def home_config(self):
        return self.load_config(default_values.cfg_path())


config = ClamNotifConfigLoader()
