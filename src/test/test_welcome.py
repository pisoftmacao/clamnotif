import logging
import os
import unittest

from clamnotif import welcome,  echo


class MockEcho(object):

    def __init__(self):
        self.trace = ""

    def welcome(self):
        self.trace = self.trace + "w"


class WelcomeTestCase(unittest.TestCase):

    def testCallEchoWelcome(self):
        self.assertEqual(welcome.echo, echo)
        welcome.echo = MockEcho()
        welcome.process()
        self.assertEqual("w", welcome.echo.trace)
        welcome.echo = echo
