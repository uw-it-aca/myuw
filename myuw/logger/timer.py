# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

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
