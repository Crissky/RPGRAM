from abc import abstractmethod
from bson import ObjectId
from datetime import datetime, timedelta
from typing import Union, Any

from repository.mongo import Database


class Model:

    def get(self, id: Union[str, ObjectId] = None, query: dict = None) -> Any:
        if id:
            if isinstance(id, str):
                query = {'player_id': id}
            elif isinstance(id, ObjectId):
                query = {'_id': id}
            else:
                raise ValueError(
                    'ID inválido. Precisa ser string ou ObjectId não vazio. '
                    f'ID: {id}, Tipo: {type(id)}'
                )
        if not query:
            raise ValueError('Query esta vazio.')
        if not isinstance(query, dict):
            raise ValueError('Query precisa ser um dicionário.')
        if (result := self.database.find(self.collection, query)):
            return self._class(**result)

    def save(self, obj: Any):
        if not isinstance(obj, self._class):
            raise ValueError(
                f'Objeto inválido. Precisa ser {self._class} não {type(obj)}'
            )
        obj_dict = obj.to_dict()
        query = {}
        if isinstance(obj._id, ObjectId):
            query['_id'] = obj._id
        else:
            obj_dict.pop('_id', None)
            if obj_dict.get('player_id'):
                query['player_id'] = obj.player_id
        if query and self.database.find(self.collection, query):
            print('Updating')
            obj_dict['updated_at'] = self.get_brazil_time_now()
            result = self.database.update(
                self.collection, query, {'$set': obj_dict}
            )
        else:
            print('Inserting')
            obj_dict['created_at'] = self.get_brazil_time_now()
            obj_dict['updated_at'] = self.get_brazil_time_now()
            result = self.database.insert(self.collection, obj_dict)

        return result

    def get_brazil_time_now(self):
        delta = timedelta(hours=3)
        dt = datetime.utcnow() - delta
        return dt

    database = property(lambda self: Database.get_instance())

    @property
    @abstractmethod
    def collection(self):
        ...

    @property
    @abstractmethod
    def _class(self):
        ...

if __name__ == '__main__':
    model = Model()
    print(model.get_brazil_time_now())