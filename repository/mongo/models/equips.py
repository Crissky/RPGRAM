from repository.mongo import CollectionEnum, Model
from repository.mongo.models.item import ItemModel
from rpgram import Equips


class EquipsModel(Model):
    _class = property(lambda self: Equips)
    collection = property(lambda self: CollectionEnum.EQUIPS.value)
    populate_fields = property(
        lambda self: {
            'helmet': {
                'id_key': 'helmet_id',
                'model': ItemModel()
            },
            'left_hand': {
                'id_key': 'left_hand_id',
                'model': ItemModel()
            },
            'right_hand': {
                'id_key': 'right_hand_id',
                'model': ItemModel()
            },
            'armor': {
                'id_key': 'armor_id',
                'model': ItemModel()
            },
            'boots': {
                'id_key': 'boots_id',
                'model': ItemModel()
            },
            'ring': {
                'id_key': 'ring_id',
                'model': ItemModel()
            },
            'amulet': {
                'id_key': 'amulet_id',
                'model': ItemModel()
            },
        }
    )


if __name__ == '__main__':
    equips_model = EquipsModel()
    equipment_model = ItemModel()
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
    amulet = equipment_model.get('999999999999999999999999')
    print(amulet)
    equips = Equips(
        player_id=123,
        _id='ffffffffffffffffffffffff',
        helmet=helmet,
        left_hand=sword,
        right_hand=shield,
        armor=armor,
        boots=boots,
        ring=ring,
        amulet=amulet,
    )
    print(equips)
    equips_model.save(equips)
    equips2 = equips_model.get('ffffffffffffffffffffffff')
    print(equips2)
