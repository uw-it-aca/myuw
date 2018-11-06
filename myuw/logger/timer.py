import time


class Timer:
    def __init__(self):
        """ Start the timer """
        self.start = time.time()

    def get_elapsed(self):
        """
        Return the time spent in seconds
        """
        return (time.time() - self.start)
