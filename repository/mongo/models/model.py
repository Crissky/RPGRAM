from abc import abstractmethod
from typing import Union, Any
from bson import ObjectId
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
        if isinstance(obj._id, ObjectId):
            query = {'_id': obj._id}
        else:
            obj_dict.pop('_id', None)
            query = {'player_id': obj.player_id}
        if self.database.find(self.collection, query):
            print('Updating')
            result = self.database.update(
                self.collection, query, {'$set': obj_dict}
            )
        else:
            result = self.database.insert(self.collection, obj_dict)

        return result

    database = property(lambda self: Database())

    @property
    @abstractmethod
    def collection(self):
        ...

    @property
    @abstractmethod
    def _class(self):
        ...
