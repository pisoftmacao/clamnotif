from .echo import echo
from .messenger import messenger


class TestSMTP(object):
    def __init__(self, _echo, _messenger):
        self.echo = _echo
        self.messenger = _messenger

    def process(self, cfg):
        receiver_address = cfg.heartbeat_receiver_addresses + \
            "," + cfg.alert_receiver_addresses
        subject = "ClamNotif Testing"
        mail_content = "Hi,\nIf you receive this email, it means ClamNotif's SMTP settings configured properly."
        self.echo.testsmtp_start()
        self.messenger.send_email(
            receiver_address, subject, mail_content, cfg)
        self.echo.testsmtp_success(cfg)


testsmtp = TestSMTP(echo, messenger)
