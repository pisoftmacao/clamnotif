from .echo import echo


class Welcome(object):

    def __init__(self, _echo):
        self.echo = _echo

    def process(self):
        self.echo.welcome()


welcome = Welcome(echo)
