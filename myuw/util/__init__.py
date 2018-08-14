from threading import Thread
import gc
from time import sleep

logger = logging.getLogger(__name__)


def check_memory():
  while(True):
    objects = gc.get_objects()
    obj_count = {}

    for obj in objects:
      if type(obj) in obj_count:
        obj_count[type(obj)] += 1
      
    logger.log(json.dumps(obj_count, indent=4, sort_keys=True)



def start_memory_thread():
  thread = Thread(target=check_memory)
  thread.start()

start_memory_thread()
