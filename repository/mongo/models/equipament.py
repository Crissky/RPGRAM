from repository.mongo import Model
from repository.mongo import CollectionEnum
from rpgram.boosters import Equipament
from rpgram.enums import DamageEnum
from rpgram.enums import EquipamentEnum


class EquipamentModel(Model):
    _class = property(lambda self: Equipament)
    collection = property(lambda self: CollectionEnum.EQUIPAMENTS.value)


if __name__ == "__main__":
    sword = Equipament(
        name='ESPADA DE AÇO TESTE MODELO',
        equip_type=EquipamentEnum.one_hand.name,
        damage_type=DamageEnum.slashing.name,
        weight=15,
        _id='ffffffffffffffffffffffff',
        bonus_strength=0,
        bonus_dexterity=0,
        bonus_constitution=0,
        bonus_intelligence=0,
        bonus_wisdom=0,
        bonus_charisma=0,
        bonus_hit_points=0,
        bonus_initiative=0,
        bonus_physical_attack=30,
        bonus_precision_attack=0,
        bonus_magical_attack=0,
        bonus_physical_defense=0,
        bonus_magical_defense=0,
        bonus_hit=15,
        bonus_evasion=-0,
    )
    equipament_model = EquipamentModel()
    print('Collection:', equipament_model.collection)
    result = equipament_model.save(sword)
    print('Result:', result)
    equipament2 = equipament_model.get('ffffffffffffffffffffffff')
    print('Equipament2:\n', equipament2)
