import datetime

def now():
    return datetime.datetime.utcnow()

class Timer:
    def __init__(self):
        """ Start the timer """
        self.start = now()

    def get_elapsed (self):
        """ Return the time spent in milliseconds """
        return (now() - self.start).microseconds / 1000
