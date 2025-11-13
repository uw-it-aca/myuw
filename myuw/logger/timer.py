# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import time


class Timer:
    def __init__(self, msg=""):
        """ Start the timer """
        self.start = time.time()
        self.msg = msg

    def get_elapsed(self):
        """
        Return the time spent in seconds
        """
        return (time.time() - self.start)
    
    def get_message(self):
        return self.msg
