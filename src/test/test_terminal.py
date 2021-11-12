import unittest

from clamnotif import echo, terminal
from .testutils import *


class TerminalTestCase(unittest.TestCase):

    def testOutputColoredText(self):
        echo.welcome()
        echo.checkcfg_file_exist_start()
        echo.checkcfg_file_exist_success()
        echo.checkcfg_file_exist_failed()
        echo.checkcfg_file_exist_failed_tips()
        echo.testsmtp_success(sample_cfg())
        terminal.success("Successfully done.")
        terminal.warning("Warning...")
        terminal.fail("Oops...")
