from repository.mongo import Model
from repository.mongo import CollectionEnum
from rpgram.boosters import Equipment
from rpgram import Consumable


class ItemModel(Model):
    _class = property(lambda self: (Equipment, Consumable))
    collection = property(lambda self: CollectionEnum.ITEMS.value)


if __name__ == "__main__":
    from rpgram.enums import DamageEnum, EquipmentEnum
    helmet = Equipment(
        name='CAPACETE DE AÇO TESTE MODELO',
        equip_type=EquipmentEnum.HELMET,
        damage_types=None,
        _id='eeeeeeeeeeeeeeeeeeeeeeee'
    )
    sword = Equipment(
        name='ESPADA DE AÇO TESTE MODELO',
        equip_type=EquipmentEnum.ONE_HAND,
        damage_types=DamageEnum.SLASHING,
        weight=15,
        requirements={'Nível': 1, 'FOR': 12},
        _id='ffffffffffffffffffffffff',
        bonus_strength=1,
        bonus_dexterity=1,
        bonus_constitution=1,
        bonus_intelligence=1,
        bonus_wisdom=1,
        bonus_charisma=1,
        bonus_hit_points=1,
        bonus_initiative=1,
        bonus_physical_attack=30,
        bonus_precision_attack=1,
        bonus_magical_attack=1,
        bonus_physical_defense=1,
        bonus_magical_defense=1,
        bonus_hit=15,
        bonus_evasion=-1,
    )
    shield = Equipment(
        name='ESCUDO DE AÇO TESTE MODELO',
        equip_type=EquipmentEnum.ONE_HAND,
        damage_types=None,
        _id='dddddddddddddddddddddddd'
    )
    armor = Equipment(
        name='ARMADURA DE AÇO TESTE MODELO',
        equip_type=EquipmentEnum.ARMOR,
        damage_types=None,
        _id='cccccccccccccccccccccccc'
    )
    boots = Equipment(
        name='BOTAS DE COURO TESTE MODELO',
        equip_type=EquipmentEnum.BOOTS,
        damage_types=None,
        _id='bbbbbbbbbbbbbbbbbbbbbbbb'
    )
    ring = Equipment(
        name='ANEL MÁGICO TESTE MODELO',
        equip_type=EquipmentEnum.RING,
        damage_types=None,
        _id='aaaaaaaaaaaaaaaaaaaaaaaa'
    )
    necklace = Equipment(
        name='COLAR BONITO TESTE MODELO',
        equip_type=EquipmentEnum.NECKLACE,
        damage_types=None,
        _id='999999999999999999999999'
    )
    potion = Consumable(
        name='Potion',
        description='Cura 100 de HP.',
        weight=0.1,
        function='target.combat_stats.hp = 100',
        _id='888888888888888888888888'
    )
    items_model = ItemModel()
    print('Collection:', items_model.collection)
    items_model.save(helmet)
    result = items_model.save(sword)
    items_model.save(shield)
    items_model.save(armor)
    items_model.save(boots)
    items_model.save(ring)
    items_model.save(necklace)
    items_model.save(potion)
    print('Result:', result)
    equipament2 = items_model.get('ffffffffffffffffffffffff')
    potion2 = items_model.get('888888888888888888888888')
    print(f'Equipament2:\n{equipament2}')
    print(f'potion2:\n{potion2}')