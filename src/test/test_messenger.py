import os
import logging
import unittest

from clamnotif import config, messenger


class MessengerTestCase(unittest.TestCase):

    @unittest.skip("Run this test after ~/.clamnotif/clamnotif.cfg is configured properly")
    def testSendHeartbeat(self):
        mail_content = "Hello, This is a simple mail for Heartbeat Testing"
        messenger.send_heartbeat(mail_content, config.home_config())
        logging.info("Heatbeat Notification Sent!")

    @unittest.skip("Run this test after ~/.clamnotif/clamnotif.cfg is configured properly")
    def testSendAlert(self):
        mail_content = "Hello, This is a simple mail for Alert Testing"
        messenger.send_alert(mail_content, config.home_config())
        logging.info("Alert Notification Sent!")
