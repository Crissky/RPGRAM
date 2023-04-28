from rpgram.boosters import StatsBooster
from rpgram.enums import EquipamentEnum, DamageEnum

class Equipament(StatsBooster):
    def __init__(
        self,
        name: str,
        equip_type: EquipamentEnum,
        damage_type: DamageEnum,
        bonus_strength: int = 0,
        bonus_dexterity: int = 0,
        bonus_constitution: int = 0,
        bonus_intelligence: int = 0,
        bonus_wisdom: int = 0,
        bonus_charisma: int = 0,
        multiplier_strength: float = 1.0,
        multiplier_dexterity: float = 1.0,
        multiplier_constitution: float = 1.0,
        multiplier_intelligence: float = 1.0,
        multiplier_wisdom: float = 1.0,
        multiplier_charisma: float = 1.0,
        bonus_hit_points: int = 0,
        bonus_initiative: int = 0,
        bonus_physical_attack: int = 0,
        bonus_ranged_attack: int = 0,
        bonus_magical_attack: int = 0,
        bonus_physical_defense: int = 0,
        bonus_magical_defense: int = 0,
        bonus_hit: int = 0,
        bonus_evasion: int = 0,
    ) -> None:
        super().__init__(
            bonus_strength=bonus_strength,
            bonus_dexterity=bonus_dexterity,
            bonus_constitution=bonus_constitution,
            bonus_intelligence=bonus_intelligence,
            bonus_wisdom=bonus_wisdom,
            bonus_charisma=bonus_charisma,
            bonus_hit_points=bonus_hit_points,
            bonus_initiative=bonus_initiative,
            multiplier_strength=multiplier_strength,
            multiplier_dexterity=multiplier_dexterity,
            multiplier_constitution=multiplier_constitution,
            multiplier_intelligence=multiplier_intelligence,
            multiplier_wisdom=multiplier_wisdom,
            multiplier_charisma=multiplier_charisma,
            bonus_physical_attack=bonus_physical_attack,
            bonus_ranged_attack=bonus_ranged_attack,
            bonus_magical_attack=bonus_magical_attack,
            bonus_physical_defense=bonus_physical_defense,
            bonus_magical_defense=bonus_magical_defense,
            bonus_hit=bonus_hit,
            bonus_evasion=bonus_evasion
        )
        self.__name = name
        self.__equip_type = equip_type
        self.__damage_type = damage_type

    def get_sheet(self) -> str:
        return (
            f'Equipamento: {self.name}\n'
            f'Tipo: {self.equip_type.value}\n'
            f'Tipo de Dano: {self.damage_type.value}\n'
        )

    def __repr__(self) -> str:
        return (
            f'########################################\n'
            f'{self.get_sheet()}'
            f'{super().get_sheet()}'
            f'########################################\n'
        )

    name = property(lambda self: self.__name)
    equip_type = property(lambda self: self.__equip_type)
    damage_type = property(lambda self: self.__damage_type)


if __name__ == '__main__':
    sword = Equipament(
        name='Espada de Aço',
        equip_type=EquipamentEnum.one_hand,
        damage_type=DamageEnum.slashing,
        bonus_strength=0,
        bonus_dexterity=0,
        bonus_constitution=0,
        bonus_intelligence=0,
        bonus_wisdom=0,
        bonus_charisma=0,
        bonus_hit_points=0,
        bonus_initiative=0,
        bonus_physical_attack=30,
        bonus_ranged_attack=0,
        bonus_magical_attack=0,
        bonus_physical_defense=0,
        bonus_magical_defense=0,
        bonus_hit=15,
        bonus_evasion=-0,
    )
    print(sword)
