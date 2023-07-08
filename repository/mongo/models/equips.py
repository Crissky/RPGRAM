from repository.mongo import CollectionEnum, Model
from repository.mongo.models.equipment import EquipmentModel
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
    equips_model = EquipsModel()
    equipment_model = EquipmentModel()
    helmet = equipment_model.get('eeeeeeeeeeeeeeeeeeeeeeee')
    print(helmet)
    sword = equipment_model.get('ffffffffffffffffffffffff')
    print(sword)
    shield = equipment_model.get('dddddddddddddddddddddddd')
    print(shield)
    armor = equipment_model.get('cccccccccccccccccccccccc')
    print(armor)
    boots = equipment_model.get('bbbbbbbbbbbbbbbbbbbbbbbb')
    print(boots)
    ring = equipment_model.get('aaaaaaaaaaaaaaaaaaaaaaaa')
    print(ring)
    necklace = equipment_model.get('999999999999999999999999')
    print(necklace)
    equips = Equips(
        _id='ffffffffffffffffffffffff',
        helmet=helmet,
        left_hand=sword,
        right_hand=shield,
        armor=armor,
        boots=boots,
        ring=ring,
        necklace=necklace,
    )
    print(equips)
    equips_model.save(equips)
    equips2 = equips_model.get('ffffffffffffffffffffffff')
    print(equips2)
