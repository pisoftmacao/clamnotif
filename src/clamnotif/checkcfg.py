import os

from .echo import echo


class CheckConfig(object):

    def __init__(self, _echo):
        self.echo = _echo

    def process(self, cfg_path):
        self.echo.welcome()
        self.echo.checkcfg_file_exist_start()
        if os.path.isfile(cfg_path):
            self.echo.checkcfg_file_exist_success()
            return
        self.echo.checkcfg_file_exist_failed()
        self.echo.checkcfg_file_exist_failed_tips()


checkcfg = CheckConfig(echo)
