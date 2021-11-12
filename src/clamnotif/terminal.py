import os


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Checklist:
    UNCHECKED = '\u2717'
    CHECKED = '\u2714'


class Layout:
    INDENT = "  "


class Terminal(object):

    def success(self, msg):
        print(Colors.OKGREEN + msg + Colors.ENDC)

    def warning(self, msg):
        print(Colors.WARNING + msg + Colors.ENDC)

    def welcome(self, msg):
        print(Colors.HEADER + msg + Colors.ENDC)

    def fail(self, msg):
        print(Colors.FAIL + msg + Colors.ENDC)

    def checked(self, msg):
        print(Layout.INDENT + "[" + Colors.OKGREEN +
              Checklist.CHECKED + Colors.ENDC + "] " + msg)

    def unchecked(self, msg):
        print(Layout.INDENT + "[" + Colors.WARNING +
              Checklist.UNCHECKED + Colors.ENDC + "] " + msg)

    def header(self, msg):
        print(Colors.BOLD + "* " + msg + Colors.ENDC)

    def please_run(self, cmd, purpose):
        print(Layout.INDENT * 3 + "Tips:")
        print(Layout.INDENT * 3 +
              "please run the following command to {}".format(purpose))
        print(Layout.INDENT * 4 + Colors.BOLD + cmd + Colors.ENDC)


terminal = Terminal()
