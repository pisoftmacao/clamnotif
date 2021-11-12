from clamnotif import config
import logging
import os

import unittest
import traceback
import sys

from .testutils import *


class ConfigurationTestCase(unittest.TestCase):
    def testLoadConfiguration(self):
        c = config.load_config(
            full_path("sample/clamnotif-sample.cfg"))
        self.assertEqual("smtp.gmail.com", c.smtp_server_host)
        self.assertEqual(587, c.smtp_server_port)
        self.assertTrue(c.smtp_tls_enabled)
        self.assertEqual("foo@gmail.com", c.sender_address)
        self.assertEqual(
            "$@SendPwd", c.sender_passwd)
        self.assertEqual(
            "My System Antivirus Notification - Alert !!!", c.alert_subject)
        self.assertEqual(
            "alice@gmail.com,robert@gmail.com,sysadmin@gmail.com", c.alert_receiver_addresses)
        self.assertEqual(
            "My System Antivirus Heartbeating Notification", c.heartbeat_subject)
        self.assertEqual(
            "sysadmin@gmail.com", c.heartbeat_receiver_addresses)
        self.assertEqual(2, c.heartbeat_day_gap)
        self.assertEqual(
            "~/.ClamAV/daily/", c.clamav_report_folder)

    def testLoadHomeConfiguration(self):
        c = config.home_config()
        self.assertFalse(c.smtp_tls_enabled)
        self.assertIsNotNone(c.smtp_server_port)
        self.assertIsNotNone(c.smtp_server_host)
        self.assertIsNotNone(c.sender_address)
        self.assertIsNotNone(c.alert_receiver_addresses)
        self.assertIsNotNone(c.alert_subject)
        self.assertIsNotNone(c.heartbeat_receiver_addresses)
        self.assertIsNotNone(c.heartbeat_subject)
        self.assertIsNotNone(c.heartbeat_day_gap)
        self.assertIsNotNone(c.clamav_report_folder)

    def testLoadConfigurationFromNonINIFile(self):
        try:
            c = config.load_config(
                full_path("sample/clamav-report-alert.log"))
            self.assertTrue(False, "Should raise an Exception above")
        except Exception as err:
            # traceback.print_tb(err.__traceback__)
            pass
