import os
import sys
import logging

from .checkreport import checkreport
from .welcome import welcome
from .testsmtp import testsmtp
from .config import config


def process_testsmtp(argv):
    cfg = config.home_config()
    if argv[1] == '--test-smtp':
        testsmtp.process(cfg)
        exit(0)
    if argv[1] == '--check-report':
        checkreport.process(cfg)
        exit(0)


def init_logger():
    logging.basicConfig(format='[clamnotif] %(asctime)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.DEBUG)


def main(argv):
    init_logger()
    if len(argv) == 1:
        welcome.process()
    if len(argv) == 2:
        process_testsmtp(argv)
    print("Usage: python3 -m clamnotif [--test-smtp|--check-report]")


if __name__ == '__main__':
    main(sys.argv)
