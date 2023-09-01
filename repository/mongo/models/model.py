from abc import abstractmethod
from bson import ObjectId
from typing import Union, Any, List
from function.datetime import get_brazil_time_now

from repository.mongo import Database
from rpgram import (
    Bag,
    Battle,
    Consumable,
    Equips,
    Group,
    Player,
)
from rpgram.boosters import (
    Classe,
    Equipment,
    Race,
)
from rpgram.characters import BaseCharacter, PlayerCharacter


def singleton(cls):
    class ClassWrapper(cls):
        _instance = None

        def __new__(c, *args, **kwargs):
            if type(c._instance) != c:
                c._instance = cls.__new__(c, *args, **kwargs)
            return c._instance
    ClassWrapper.__name__ = cls.__name__
    return ClassWrapper


@singleton
class Model:
    '''Classe Base usada para salvar Classes no Banco de Dados MongoDB'''

    def __alt_id_is_valid(self):
        return isinstance(self.alternative_id, str)

    def delete(
        self,
        _id: Union[int, ObjectId, str] = None,
        query: dict = None
    ) -> Any:
        if _id:
            if isinstance(_id, ObjectId):
                query = {'_id': _id}
            elif ObjectId.is_valid(_id):
                query = {'_id': ObjectId(_id)}
            elif isinstance(_id, (int, str)) and self.__alt_id_is_valid():
                query = {self.alternative_id: _id}
            else:
                raise ValueError(
                    'ID inválido. O ID Precisa ser um inteiro ou ObjectId ou '
                    'uma string com 24 caracteres que representa um ObjectId.'
                    f'ID: {_id}, Tipo: {type(_id)}'
                )
        if not query:
            raise ValueError('Query esta vazia.')
        if not isinstance(query, dict):
            raise ValueError('Query precisa ser um dicionário.')
        return self.database.delete(self.collection, query)

    def get(
        self,
        _id: Union[int, ObjectId, str] = None,
        query: dict = None,
        fields: Union[dict, list, str] = None,
        partial: bool = True
    ) -> Any:
        if _id:
            if isinstance(_id, ObjectId):
                query = {'_id': _id}
            elif ObjectId.is_valid(_id):
                query = {'_id': ObjectId(_id)}
            elif isinstance(_id, (int, str)) and self.__alt_id_is_valid():
                query = {self.alternative_id: _id}
            else:
                raise ValueError(
                    'ID inválido. O ID Precisa ser um inteiro ou ObjectId ou '
                    'uma string com 24 caracteres que representa um ObjectId.'
                    f'ID: {_id}, Tipo: {type(_id)}'
                )
        if not query:
            raise ValueError('Query esta vazia.')
        if not isinstance(query, dict):
            raise ValueError('Query precisa ser um dicionário.')
        if isinstance(fields, str):
            fields = [fields]
        if (result := self.database.find(self.collection, query, fields)):
            if fields and partial:
                return result
            populate_result = self.__populate_load(result)
            return self.instanciate_class(populate_result)

    def get_all(
        self, query: dict = None, fields: Union[dict, list, str] = None
    ) -> List[Union[dict, str]]:

        if isinstance(fields, str):
            fields = [fields]

        result = self.database.find_many(self.collection, query, fields)

        if not fields:
            result = [
                self.instanciate_class(self.__populate_load(item))
                for item in result
            ]
        elif len(fields) == 1:
            result = [item[fields[0]] for item in result]
        else:
            result = list(result)

        return result

    def save(self, obj: Any):
        if not isinstance(obj, self._class):
            raise ValueError(
                f'Objeto inválido. Precisa ser {self._class} não {type(obj)}'
            )
        obj_dict = obj.to_dict()
        obj_dict['_class'] = obj.__class__.__name__
        query = {}
        if isinstance(obj._id, ObjectId):
            query['_id'] = obj._id
        else:
            obj_dict.pop('_id', None)
            if obj_dict.get(self.alternative_id, None):
                query[self.alternative_id] = obj_dict[self.alternative_id]
        if query and self.database.find(self.collection, query):
            print(f'Updating: {self.__class__.__name__}')
            obj_dict['updated_at'] = get_brazil_time_now()
            result = self.database.update(
                self.collection, query, {'$set': obj_dict}
            )
        else:
            print(f'Inserting: {self.__class__.__name__}')
            obj_dict['created_at'] = get_brazil_time_now()
            obj_dict['updated_at'] = get_brazil_time_now()
            result = self.database.insert(self.collection, obj_dict)

        return result

    def __populate_load(self, dict_obj: dict):
        '''Função que popula os campos do objeto que são outras classes e que 
        no banco são salvos somente a sua chave. Esses campo que serão 
        populados pertencem a outra tabela e por conta disso
        devem possuir sua própria classe Model.

        Quando o campo a ser populado é uma lista, todos os elementos da lista 
        serão populados, porém todos eles devem pertencer a mesma tabela.'''
        for field_name, field_info in self.populate_fields.items():
            if field_info['id_key'] in dict_obj.keys():
                key = field_info['id_key']
                dict_field = dict_obj.pop(key)
                model = field_info['model']

                object = None
                if isinstance(dict_field, list):
                    object = []
                    for item in dict_field:
                        if isinstance(item, dict):
                            object_id = item.pop('_id')
                            object_loaded = model.get(object_id)
                            if 'subclass' in field_info.keys():
                                subclass = field_info['subclass']
                                object_loaded = subclass(object_loaded, **item)
                            object.append(object_loaded)
                        elif isinstance(item, (ObjectId, str)):
                            object.append(model.get(item))
                        else:
                            raise KeyError(
                                f'O valor da id_key "{key}" no "dict_obj" '
                                f'é uma lista e um elemento dessa lista não é '
                                f'um dict com o campo "_id", str ou ObjectId. '
                                f'item: {item}.'
                            )
                elif dict_field is not None:  # esperado que dict_field seja um _id
                    object = model.get(dict_field)

                dict_obj[field_name] = object
            else:
                if isinstance(self._class, tuple):
                    class_name = ', '.join([c.__name__ for c in self._class])
                else:
                    class_name = self._class.__name__
                raise KeyError(
                    f'O dicionário da(s) classe(s) {class_name} '
                    f'não possui campo {field_info["id_key"]}.'
                )

        return dict_obj

    def instanciate_class(self, populate_result: dict):
        _class = eval(populate_result.pop('_class'))
        return _class(**populate_result)

    database: Database = property(lambda self: Database.get_instance())
    alternative_id: str = property(lambda self: 'player_id')

    @property
    @abstractmethod
    def collection(self) -> str:
        ...

    @property
    @abstractmethod
    def _class(self) -> Any:
        ...

    @property
    def populate_fields(self) -> dict:
        '''
            Retorna um dicionário com os campos necessários para criar
            os objetos de outros modelos necessários para o modelo atual.

            field_name: Nome do campo que será populado ao criar o objeto.
                id_key: caminho do campo usando para buscar o objeto no banco
                    (aka _id ou alternative_id).
                model: Modelo usado para carregar o objeto que populará
                    o objeto do modelo atual.
                subclass: Class que será usada para instanciar o novo objeto
                    que usará o objeto carregado pelo `model` quando campo é
                    salvo no banco do objeto pai com o tipo lista.

            populate_fields = {
                'field_name': {
                    'id_key': string,
                    'model': Model,
                    'subclass': Any Class,
                },
                ...
            }
            Exemplo:
            populate_fields = {
                'race': {
                    'id_key': 'race_name',
                    'model': RaceModel,
                }
            }
            Exemplo2:
            populate_fields = {
                'items': {
                    'id_key': 'items_ids',
                    'model': ItemModel(),  # Carrega equipamentos e consumíveis
                    'subclass': Item
                }
           }
    )
        '''
        return {}
