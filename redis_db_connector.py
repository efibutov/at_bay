"""API for accessing Redis-DB"""
import redis
import settings
import json


class DataBaseConnector(object):
    """
    Basic RedisDB interface.
    Please, note, that every provided value should be a dictionary
    """
    def __init__(self):
        self.__db = redis.Redis(
            host=settings.REDIS_DB_HOST,
            port=settings.REDIS_DB_PORT,
            db=settings.REDIS_DB_INDEX
        )

    def set(self, key, value):
        """
        Saves a string-representation of value (in dictionary form)
        under provided key
        """
        self.__db.set(key, value, ex=settings.REDIS_DB_KEY_TTL)

    def get(self, key):
        """
        Gets saved value (defined by the key) and converts it to dictionary
        Return empty dictionary if the key does not exist
        """
        value = self.__db.get(key)

        if value:
            return json.loads(value)
        else:
            return {'status': 'Not-Found'}
