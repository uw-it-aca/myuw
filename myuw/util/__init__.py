from threading import Thread
from time import sleep
import gc
import json
import logging
import sys

logger = logging.getLogger(__name__)


def check_memory():
    while(True):
        objects = gc.get_objects()
        obj_count = {}

        for obj in objects:
            if str(type(obj)) in obj_count:
                obj_count[str(type(obj))][0] += 1 
                obj_count[str(type(obj))][1] +=  sys.getsizeof(obj) 
            else:
                obj_count[str(type(obj))] = [1, sys.getsizeof(obj)]

        logger.error(json.dumps(obj_count, indent=4, sort_keys=True))
        sleep(5)


def start_memory_thread():
    thread = Thread(target=check_memory)
    thread.start()

start_memory_thread()
