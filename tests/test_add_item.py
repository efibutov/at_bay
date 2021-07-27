import time
import requests as rq
import web_server
import task_queue
import redis_db_connector
from ..system_manager import SystemManager
from ..settings import AVAILABLE_STATUSES, WEB_SERVER_HOST, WEB_SERVER_PORT

BACKEND_URL = f'http://{WEB_SERVER_HOST}:{WEB_SERVER_PORT}'


class DataBaseConnector(object):
    def __init__(self):
        pass

    def set(self, key, value):
        pass

    def get(self, key):
        return {'status': 'Not-Found'}


class TaskQueue(object):
    def __init__(self):
        pass

    def put(self, value):
        pass

    def consume(self):
        return {'task_id': 'a' * 36}


def get_unique_id():
    return 'a' * 36


def test_add_item_verify_status(monkeypatch):
    monkeypatch.setattr(web_server, 'get_unique_id', get_unique_id)
    monkeypatch.setattr(redis_db_connector, 'DataBaseConnector', DataBaseConnector)
    monkeypatch.setattr(task_queue, 'TaskQueue', TaskQueue)

    with SystemManager() as sm:
        time.sleep(0.005)
        task_id = rq.post(
            url=f'{BACKEND_URL}/task',
            json={"url": "https://www.google.com"}
        ).json()['task_id']

        assert task_id == 'a' * 36

        status = rq.get(
            f'{BACKEND_URL}/status/{task_id}'
        ).json()['status']

    assert status in AVAILABLE_STATUSES
