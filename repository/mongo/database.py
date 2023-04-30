from pymongo import MongoClient
from decouple import config

URL_CONNECTION = config('URL_CONNECTION')
DATABASE_NAME = config('DATABASE_NAME')


class Database:
    _instance = None

    def __init__(self, url_connection, database_name):
        self.__client = MongoClient(
            url_connection, serverSelectionTimeoutMS=5000
        )
        self.__server_info = self.__client.server_info()
        self.__database = self.__client[database_name]

    def insert(self, collection, data):
        return self.database[collection].insert_one(data)

    def find(self, collection, query):
        return self.database[collection].find_one(query)

    def find_many(self, collection, query):
        return self.database[collection].find(query)

    def update(self, collection, query, data):
        return self.database[collection].update_one(query, data)

    def delete(self, collection, query):
        return self.database[collection].delete_one(query)

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = Database(URL_CONNECTION, DATABASE_NAME)
        return cls._instance

    database = db = property(lambda self: self.__database)
    server_info = property(lambda self: self.__server_info)


if __name__ == '__main__':
    print(Database.get_instance())
