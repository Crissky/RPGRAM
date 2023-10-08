from bson import ObjectId
from datetime import datetime

from constant.text import TEXT_DELIMITER
from function.text import escape_basic_markdown_v2, remove_bold, remove_code

from rpgram.equips import Equips
from rpgram.status import Status
from rpgram.boosters.classe import Classe
from rpgram.boosters.race import Race
from rpgram.constants.text import (
    CHARACTER_EMOJI_TEXT,
    CLASS_EMOJI_TEXT,
    RACE_EMOJI_TEXT
)
from rpgram.stats import BaseStats, CombatStats


class BaseCharacter:
    def __init__(
        self,
        char_name: str,
        classe: Classe,
        race: Race,
        player_id: int = None,
        equips: Equips = None,
        status: Status = None,
        level: int = 1,
        xp: int = 0,
        base_strength: int = 0,
        base_dexterity: int = 0,
        base_constitution: int = 0,
        base_intelligence: int = 0,
        base_wisdom: int = 0,
        base_charisma: int = 0,
        combat_damage: int = 0,
        _id: ObjectId = None,
        created_at: datetime = None,
        updated_at: datetime = None
    ) -> None:
        if isinstance(_id, str):
            _id = ObjectId(_id)
        if equips is None:
            equips = Equips(player_id=player_id, _id=ObjectId())
        if status is None:
            status = Status(player_id=player_id, _id=ObjectId())

        self.__name = char_name
        self.__id = _id
        self.__classe = classe
        self.__race = race
        self.__equips = equips
        self.__status = status
        self.__base_stats = BaseStats(
            level=level,
            xp=xp,
            base_strength=base_strength,
            base_dexterity=base_dexterity,
            base_constitution=base_constitution,
            base_intelligence=base_intelligence,
            base_wisdom=base_wisdom,
            base_charisma=base_charisma,
            stats_boosters=[self.__race, self.__classe, self.__equips]
        )
        self.__combat_stats = CombatStats(
            base_stats=self.__base_stats,
            damage=combat_damage
        )
        self.__equips.attach_observer(self.__base_stats)
        self.__equips.attach_observer(self.__combat_stats)
        self.__status.attach_observer(self.__base_stats)
        self.__status.attach_observer(self.__combat_stats)
        self.__created_at = created_at
        self.__updated_at = updated_at

    def is_damaged(self) -> bool:
        return self.combat_stats.damaged

    def is_healed(self) -> bool:
        return self.combat_stats.healed

    def is_alive(self) -> bool:
        return self.combat_stats.alive

    def is_dead(self) -> bool:
        return self.combat_stats.dead

    # Getters
    name: str = property(lambda self: self.__name)
    _id: ObjectId = property(lambda self: self.__id)
    base_stats: BaseStats = property(fget=lambda self: self.__base_stats)
    combat_stats: CombatStats = property(fget=lambda self: self.__combat_stats)
    classe: Classe = property(fget=lambda self: self.__classe)
    race: Race = property(fget=lambda self: self.__race)
    equips: Equips = property(fget=lambda self: self.__equips)
    status: Status = property(fget=lambda self: self.__status)
    created_at: datetime = property(lambda self: self.__created_at)
    updated_at: datetime = property(lambda self: self.__updated_at)
    bs = base_stats
    cs = combat_stats

    def get_sheet(self, verbose: bool = False, markdown: bool = False) -> str:
        text = f'*{CHARACTER_EMOJI_TEXT}*: {self.name}\n'
        if verbose:
            text += f'*ID Personagem*: {self.__id}\n'

        if not markdown:
            text = remove_bold(text)
            text = remove_code(text)
        else:
            text = escape_basic_markdown_v2(text)

        return text

    def get_all_sheets(
        self, verbose: bool = False, markdown: bool = False
    ) -> str:
        if verbose:
            text = (
                f'{self.get_sheet(verbose, markdown)}'
                f'{self.status.get_all_sheets(verbose, markdown)}\n'
                f'{self.base_stats.get_sheet(verbose, markdown)}\n'
                f'{self.combat_stats.get_sheet(verbose, markdown)}\n'
                f'{self.race.get_sheet(verbose, markdown)}\n'
                f'{self.classe.get_sheet(verbose, markdown)}\n'
                f'{self.equips.get_sheet(verbose, markdown)}\n'
            )
        else:
            # Trecho feito dessa forma para o escape_basic_markdown_v2 não ser
            # usado duas vezes nos textos que vem dos outros get_sheet, pois
            # o esperado seria somente uma \ e não duas.
            race_classe_text = (
                f'*{RACE_EMOJI_TEXT}*: {self.race.name}\n'
                f'*{CLASS_EMOJI_TEXT}*: {self.classe.name}\n'
            )
            if not markdown:
                race_classe_text = remove_bold(race_classe_text)
                race_classe_text = remove_code(race_classe_text)
            else:
                race_classe_text = escape_basic_markdown_v2(race_classe_text)
            text = (
                f'{self.get_sheet(verbose, markdown)}'
                f'{self.status.get_all_sheets(verbose, markdown)}\n'
                f'{race_classe_text}'
                f'{self.base_stats.get_sheet(verbose, markdown)}\n'
                f'{self.combat_stats.get_sheet(verbose, markdown)}\n'
                f'{self.equips.get_sheet(verbose, markdown)}'
            )

        return text

    def __str__(self) -> str:
        return (
            f'{TEXT_DELIMITER}\n'
            f'{self.get_all_sheets(True)}'
            f'{TEXT_DELIMITER}\n'
        )

    def __repr__(self) -> str:
        return (
            f'<Personagem: "{self.name} '
            f'({self.classe.name}/{self.race.name})", '
            f'HP: {self.cs.current_hit_points}/{self.cs.hit_points}>'
        )

    def to_dict(self):
        return dict(
            char_name=self.name,
            _id=self.__id,
            level=self.base_stats.level,
            xp=self.base_stats.xp,
            base_strength=self.base_stats.base_strength,
            base_dexterity=self.base_stats.base_dexterity,
            base_constitution=self.base_stats.base_constitution,
            base_intelligence=self.base_stats.base_intelligence,
            base_wisdom=self.base_stats.base_wisdom,
            base_charisma=self.base_stats.base_charisma,
            combat_damage=(self.cs.hit_points - self.cs.current_hit_points),
            race_name=self.race.name,
            classe_name=self.classe.name,
            equips_id=self.equips._id,
            status_id=self.status._id,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, BaseCharacter):
            if self._id is not None and other._id is not None:
                return all((
                    self.__id == other.__id,
                    self.name == other.name,
                ))
        return False


if __name__ == '__main__':
    from rpgram.boosters import Equipment
    from rpgram.enums import DamageEnum, EquipmentEnum
    helmet = Equipment(
        name='Capacete de Aço',
        equip_type=EquipmentEnum.HELMET,
        damage_types=None,
        weight=10,
        bonus_physical_defense=30,
        bonus_evasion=-5,
    )
    sword = Equipment(
        name='Espada Gigante de Aço',
        equip_type=EquipmentEnum.TWO_HANDS,
        damage_types=DamageEnum.SLASHING,
        weight=40,
        bonus_physical_attack=30,
        bonus_hit=15,
        bonus_evasion=-10,
    )
    armor = Equipment(
        name='Armadura de Aço',
        equip_type=EquipmentEnum.ARMOR,
        damage_types=None,
        weight=60,
        bonus_physical_defense=80,
        bonus_evasion=-25,
    )
    boots = Equipment(
        name='Botas de Couro',
        equip_type=EquipmentEnum.BOOTS,
        damage_types=None,
        weight=10,
        bonus_physical_defense=10,
        bonus_magical_defense=10,
        bonus_evasion=30,
    )
    ring = Equipment(
        name='Algum Anel',
        equip_type=EquipmentEnum.RING,
        damage_types=None,
        weight=0.1,
        bonus_evasion=100,
    )
    amulet = Equipment(
        name='Colar Brilhante',
        equip_type=EquipmentEnum.AMULET,
        damage_types=None,
        weight=0.2,
        bonus_charisma=150,
    )
    equips = Equips(
        player_id=123,
        helmet=helmet,
        left_hand=sword,
        armor=armor,
        boots=boots,
        ring=ring,
        amulet=amulet,
    )
    classe = Classe(
        name='Arqueiro',
        description='Arqueiro Teste',
        bonus_strength=5,
        bonus_dexterity=15,
        bonus_constitution=10,
        bonus_intelligence=10,
        bonus_wisdom=10,
        bonus_charisma=10,
        multiplier_strength=1,
        multiplier_dexterity=1.5,
        multiplier_constitution=1,
        multiplier_intelligence=1,
        multiplier_wisdom=1,
        multiplier_charisma=1,
    )
    race = Race(
        name='Elfo',
        description='Elfo Teste',
        bonus_strength=8,
        bonus_dexterity=12,
        bonus_constitution=8,
        bonus_intelligence=10,
        bonus_wisdom=12,
        bonus_charisma=10,
        multiplier_strength=1.0,
        multiplier_dexterity=1.0,
        multiplier_constitution=1.0,
        multiplier_intelligence=1.2,
        multiplier_wisdom=1.2,
        multiplier_charisma=1.0,
    )
    base_character = BaseCharacter(
        char_name='Personagem Teste',
        classe=classe,
        race=race,
        equips=equips,
        _id='ffffffffffffffffffffffff',
        level=21,
        xp=0,
        base_strength=10,
        base_dexterity=10,
        base_constitution=10,
        base_intelligence=10,
        base_wisdom=10,
        base_charisma=10,
        combat_damage=0,
    )
    print(base_character)
    base_character.base_stats.xp = 100
    base_character.base_stats.dexterity = 1
    base_character.combat_stats.hp = -100
    base_character.combat_stats.hit_points = 50
    print(base_character)
    print(base_character.to_dict())
