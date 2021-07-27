"""Queue of tasks - both for adding and poping"""
import settings
from hotqueue import HotQueue


class TaskQueue(object):
    def __init__(self):
        self.__task_queue = HotQueue(
            name=settings.TASK_QUEUE_NAME,
            host=settings.REDIS_DB_HOST,
            port=settings.REDIS_DB_PORT,
            db=settings.REDIS_DB_INDEX
        )

    def put(self, value):
        """Put new value (id of the item in the RedisDB)"""
        self.__task_queue.put(value)

    def consume(self):
        """Pop an item from the Queue"""
        return self.__task_queue.consume()
