import unittest

from clamnotif import echo, messenger, testsmtp, config
from .testutils import *


class MockEcho(object):
    def __init__(self):
        self.trace = ""

    def testsmtp_start(self):
        self.trace = self.trace + "st"

    def testsmtp_success(self, cfg):
        self.trace = self.trace + "_s"
        self.cfg = cfg


class MockMessenger(object):
    def __init__(self):
        self.trace = ""

    def send_email(self, receiver_address, subject, mail_content, config):
        self.trace = self.trace + "s"
        self.receiver_address = receiver_address
        self.subject = subject
        self.mail_content = mail_content
        self.config = config


class TestSMTPTestCase(unittest.TestCase):

    def testSendSampleEail(self):
        self.assertEqual(testsmtp.echo, echo)
        self.assertEqual(testsmtp.messenger, messenger)
        testsmtp.echo = MockEcho()
        testsmtp.messenger = MockMessenger()
        cfg = sample_cfg()
        testsmtp.process(cfg)
        self.assertEqual("st_s", testsmtp.echo.trace)
        self.assertEqual("s", testsmtp.messenger.trace)
        self.assertEqual(cfg.heartbeat_receiver_addresses + "," +
                         cfg.alert_receiver_addresses, testsmtp.messenger.receiver_address)
        self.assertEqual("ClamNotif Testing", testsmtp.messenger.subject)
        self.assertEqual(
            "Hi,\nIf you receive this email, it means ClamNotif's SMTP settings configured properly.", testsmtp.messenger.mail_content)
        self.assertEqual(cfg, testsmtp.messenger.config)
        self.assertEqual(cfg, testsmtp.echo.cfg)
        testsmtp.echo = echo
        testsmtp.messenger = messenger
