from typing import Any, Union
from pymongo import MongoClient
from pymongo.cursor import Cursor
from pymongo.results import InsertOneResult, UpdateResult, DeleteResult

from decouple import config

URL_CONNECTION = config('URL_CONNECTION')
DATABASE_NAME = config('DATABASE_NAME')


class Database:
    _instance = None

    def __init__(self, url_connection: str, database_name: str) -> None:
        self.__client = MongoClient(
            url_connection, serverSelectionTimeoutMS=5000
        )
        self.__server_info = self.__client.server_info()
        self.__database = self.__client[database_name]

    def insert(self, collection: str, data: dict) -> InsertOneResult:
        return self.database[collection].insert_one(document=data)

    def find(
        self, collection: str, query: dict, fields: Union[list, dict] = None
    ) -> Union[dict, None]:
        return self.database[collection].find_one(
            filter=query, projection=fields
        )

    def find_many(
        self,
        collection: str,
        query: dict,
        fields: Union[list, dict] = None
    ) -> Cursor:
        return self.database[collection].find(filter=query, projection=fields)

    def update(self, collection: str, query: dict, data: dict) -> UpdateResult:
        return self.database[collection].update_one(filter=query, update=data)

    def replace(
        self,
        collection: str,
        query: dict,
        data: dict,
        upsert: bool = True
    ) -> UpdateResult:
        return self.database[collection].replace_one(
            filter=query,
            replacement=data,
            upsert=upsert
        )

    def delete(self, collection: str, query: dict) -> DeleteResult:
        return self.database[collection].delete_one(filter=query)

    def count(self, collection: str, query: dict, **kwargs: Any) -> int:
        return self.db[collection].count_documents(filter=query, **kwargs)

    def length(self, collection: str, query: dict, field: str) -> int:
        cursor = self.db[collection].aggregate([
            {
                '$match': query
            },
            {
                '$project': {
                    'length': {
                        '$size': f'${field}'
                    }
                }
            }
        ])
        result = next(cursor, None)
        if result:
            return result['length']

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = Database(URL_CONNECTION, DATABASE_NAME)
        return cls._instance

    database = db = property(lambda self: self.__database)
    server_info = property(lambda self: self.__server_info)


if __name__ == '__main__':
    print(Database.get_instance())
