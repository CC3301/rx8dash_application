import signal


# signal handler
class SignalHandler:
    def __init__(self, app):

        self.app = app
        signal.signal(signal.SIGINT, self._sigint_handler)

    def _sigint_handler(self, signum, frame):
        self.app.stop()
    
