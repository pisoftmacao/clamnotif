import os


class DefaultValues(object):
    def cfg_path(self):
        return os.path.expanduser("~/.clamnotif/clamnotif.cfg")

    def lastlog_path(self):
        return os.path.expanduser("~/.clamnotif/lastlog.json")


default_values = DefaultValues()
