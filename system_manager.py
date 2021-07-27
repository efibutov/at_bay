from web_server import WebServer
from processor import Processor
import settings


class SystemManager(object):
    def __init__(self):
        self.__web_server = WebServer(
            host=settings.WEB_SERVER_HOST,
            port=settings.WEB_SERVER_PORT
        )
        self.__processor = Processor()

    def stop(self):
        self.__web_server.stop()
        self.__processor.stop()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.stop()
