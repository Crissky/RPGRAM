from abc import abstractmethod
from bson import ObjectId
from typing import Union, Any
from functions.datetime import get_brazil_time_now

from repository.mongo import Database


class Model:
    '''Classe Base usada para salvar Classes no Banco de Dados MongoDB'''

    def get(self, id: Union[int, ObjectId] = None, query: dict = None) -> Any:
        if id:
            if isinstance(id, int):
                query = {self.alternative_id: id}
            elif isinstance(id, ObjectId):
                query = {'_id': id}
            else:
                raise ValueError(
                    'ID inválido. Precisa ser inteiro ou ObjectId não vazio. '
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
            if obj_dict.get(self.alternative_id, None):
                query[self.alternative_id] = obj_dict[self.alternative_id]
        if query and self.database.find(self.collection, query):
            print('Updating')
            obj_dict['updated_at'] = get_brazil_time_now()
            result = self.database.update(
                self.collection, query, {'$set': obj_dict}
            )
        else:
            print('Inserting')
            obj_dict['created_at'] = get_brazil_time_now()
            obj_dict['updated_at'] = get_brazil_time_now()
            result = self.database.insert(self.collection, obj_dict)

        return result

    database = property(lambda self: Database.get_instance())
    alternative_id = property(lambda self: 'player_id')

    @property
    @abstractmethod
    def collection(self):
        ...

    @property
    @abstractmethod
    def _class(self):
        ...
