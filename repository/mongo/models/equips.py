from repository.mongo import CollectionEnum, Model, EquipmentModel
from rpgram import Equips


class EquipsModel(Model):
    _class = property(lambda self: Equips)
    collection = property(lambda self: CollectionEnum.EQUIPS.value)
    populate_fields = property(
        lambda self: {
            'helmet': {
                'id_key': 'helmet_id',
                'model': EquipmentModel()
            },
            'left_hand': {
                'id_key': 'left_hand_id',
                'model': EquipmentModel()
            },
            'right_hand': {
                'id_key': 'right_hand_id',
                'model': EquipmentModel()
            },
            'armor': {
                'id_key': 'armor_id',
                'model': EquipmentModel()
            },
            'boots': {
                'id_key': 'boots_id',
                'model': EquipmentModel()
            },
            'ring': {
                'id_key': 'ring_id',
                'model': EquipmentModel()
            },
            'necklace': {
                'id_key': 'necklace_id',
                'model': EquipmentModel()
            },
        }
    )

if __name__ == '__main__':
    ...