"""
Web-server (with REST API): accepts new item, create a unique ID, and signalize
to workers there is a new item, and adds the item to Redis-DB.
Second end-point (status) returns a status of requested item.
"""
import json
import uuid
from flask import Flask, request
from flask_restful import Resource, Api
from multiprocessing import Process
from redis_db_connector import DataBaseConnector
from task_queue import TaskQueue


def get_unique_id():
    return str(uuid.uuid4())


class WebServer(object):
    db = DataBaseConnector()
    task_queue = TaskQueue()

    class GetTaskInfo(Resource):
        def get(self, task_id):
            """Get item's status, identified by its unique id,
            generated on adding the item to the system"""
            return WebServer.db.get(task_id)

    class AddNewTask(Resource):
        def post(self):
            """Add new item to the system"""
            try:
                url = json.loads(request.data)['url']
            except Exception as e:
                return {'error': e.args}
            else:
                key = get_unique_id()
                value = json.dumps({
                    'url': url,
                    'status': 'Accepted'
                })
                WebServer.db.set(key=key, value=value)
                WebServer.task_queue.put(key)
                return {'task_id': key}

    def __init__(self, host='localhost', port=5000):
        """Run the web server in a separate process"""
        self.__host = host
        self.__port = port
        self.__server_process = Process(target=self.__run)
        self.__server_process.start()

    def __run(self):
        self.__app = Flask(__name__)
        self.__api = Api(self.__app)
        self.__api.add_resource(self.GetTaskInfo, '/status/<task_id>')
        self.__api.add_resource(self.AddNewTask, '/task/')
        self.__app.run(host=self.__host, port=self.__port, debug=False)

    def stop(self):
        self.__server_process.kill()
        self.__server_process.join()
