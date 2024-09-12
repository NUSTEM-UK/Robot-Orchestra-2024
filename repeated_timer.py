from threading import Timer

class RepeatedTimer(object):
    """Simple timer class, from StackExchange (obviously).

    Credit: user MestreLion, https://stackoverflow.com/questions/3393612

    Modified to allow change of interval without tearing down the timer.
    """

    def __init__(self, interval, function, *args):
        """Initialize the timer object."""
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.is_running = False
        self.start()

    def _run(self):
        """Timer has been triggered: execute callback function."""
        self.is_running = False
        self.start()
        self.function(*self.args)

    def start(self):
        """Start the timer, if it's not already running."""
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        """Stop the timer."""
        self._timer.cancel()
        self.is_running = False

    def bpm(self, newBPM):
        """Reset the interval to new beats per minute."""
        self.interval = (60/newBPM)
