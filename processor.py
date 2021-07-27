"""
Manages scanning of resources in parallel and updating status in the DB
"""
import json
import random
import settings
from task_queue import TaskQueue
from threading import Thread
from multiprocessing import Process
from redis_db_connector import DataBaseConnector
from concurrent.futures import ThreadPoolExecutor


class Processor(object):
    """Processing items unit"""
    def __init__(self):
        self.__queue = TaskQueue()
        self.__db_connector = DataBaseConnector()
        self.__listener = Process(target=self.__process_items)
        self.__listener.start()

    def __process_items(self):
        """Spawn a new worker when a new task has been received"""
        with ThreadPoolExecutor(max_workers=settings.NUM_OF_WORKERS) as executor:
            for key in self.__queue.consume():
                executor.submit(self.__scan_item, key=key)

    def __scan_item(self, key):
        """
        Scan the item and update its status in the DB
        (random choise among list of available statuses)
        """
        item = self.__db_connector.get(key)
        item['status'] = random.choice(settings.AVAILABLE_STATUSES)
        self.__db_connector.set(key=key, value=json.dumps(item))

    def stop(self):
        self.__listener.kill()
        self.__listener.join()
