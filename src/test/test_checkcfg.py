import logging
import os
import unittest

from clamnotif import checkcfg, config, echo
from .testutils import *


class MockEcho(object):

    def __init__(self):
        self.trace = ""

    def welcome(self):
        self.trace = self.trace + "w"

    def checkcfg_file_exist_start(self):
        self.trace = self.trace + "_fe_start"

    def checkcfg_file_exist_success(self):
        self.trace = self.trace + "_fe_success"

    def checkcfg_file_exist_failed(self):
        self.trace = self.trace + "_fe_failed"

    def checkcfg_file_exist_failed_tips(self):
        self.trace = self.trace + "_fe_tips"


class CheckCfgTestCase(unittest.TestCase):

    def testConfigFileExists(self):
        cfg_path = full_path("sample/clamnotif-sample.cfg")
        self.assertEqual(checkcfg.echo, echo)
        checkcfg.echo = MockEcho()
        checkcfg.process(cfg_path)
        self.assertEqual("w_fe_start_fe_success", checkcfg.echo.trace)
        checkcfg.echo = echo

    def testConfigFileNotExists(self):
        cfg_path = full_path("sample/noexist-sample.cfg")
        self.assertEqual(checkcfg.echo, echo)
        checkcfg.echo = MockEcho()
        checkcfg.process(cfg_path)
        self.assertEqual("w_fe_start_fe_failed_fe_tips", checkcfg.echo.trace)
        checkcfg.echo = echo
