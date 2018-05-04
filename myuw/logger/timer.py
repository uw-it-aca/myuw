import time


class Timer:
    def __init__(self):
        """ Start the timer """
        self.start = self._now()

    def _now(self):
        return time.time()

    def get_elapsed(self):
        """
        Return the time spent in seconds
        """
        return (self._now() - self.start)
