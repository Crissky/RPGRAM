from datetime import datetime
from statistics import mean
from typing import Iterable, Iterator, List, Union

from bson import ObjectId

from constant.text import SECTION_HEAD, TEXT_DELIMITER, TEXT_SEPARATOR
from function.text import escape_basic_markdown_v2, remove_bold, remove_code

from rpgram.boosters.equipment import Equipment
from rpgram.constants.text import (
    CHARISMA_EMOJI_TEXT,
    CONSTITUTION_EMOJI_TEXT,
    DEXTERITY_EMOJI_TEXT,
    EVASION_EMOJI_TEXT,
    HIT_EMOJI_TEXT,
    HIT_POINT_FULL_EMOJI_TEXT,
    INITIATIVE_EMOJI_TEXT,
    INTELLIGENCE_EMOJI_TEXT,
    MAGICAL_ATTACK_EMOJI_TEXT,
    MAGICAL_DEFENSE_EMOJI_TEXT,
    PHYSICAL_ATTACK_EMOJI_TEXT,
    PHYSICAL_DEFENSE_EMOJI_TEXT,
    PRECISION_ATTACK_EMOJI_TEXT,
    STRENGTH_EMOJI_TEXT,
    WISDOM_EMOJI_TEXT
)
from rpgram.enums.emojis import EmojiEnum
from rpgram.enums.equipment import EquipmentEnum
from rpgram.errors import EquipmentRequirementError
from rpgram.skills.special_damage import SpecialDamage
from rpgram.stats.stats_base import BaseStats

if __name__ in ['__main__', 'equip']:
    from rpgram.enums import DamageEnum


class Equips:
    '''Classe responsável por armazenar os equipamentos do jogador'''

    def __init__(
        self,
        player_id: int,
        _id: Union[str, ObjectId] = None,
        helmet: Equipment = None,
        left_hand: Equipment = None,
        right_hand: Equipment = None,
        armor: Equipment = None,
        boots: Equipment = None,
        ring: Equipment = None,
        amulet: Equipment = None,
        created_at: datetime = None,
        updated_at: datetime = None
    ) -> None:
        if isinstance(_id, str):
            _id = ObjectId(_id)

        self.__player_id = player_id
        self.__id = _id

        self.__helmet = None
        self.__left_hand = None
        self.__right_hand = None
        self.__armor = None
        self.__boots = None
        self.__ring = None
        self.__amulet = None

        self.__observers = []

        self.__created_at = created_at
        self.__updated_at = updated_at

        self.__init = True

        if isinstance(helmet, Equipment):
            self.equip(helmet)
        if isinstance(left_hand, Equipment):
            self.equip(left_hand, 'LEFT')
        if isinstance(right_hand, Equipment):
            if right_hand.equip_type != EquipmentEnum.TWO_HANDS:
                self.equip(right_hand, 'RIGHT')
        if isinstance(armor, Equipment):
            self.equip(armor)
        if isinstance(boots, Equipment):
            self.equip(boots)
        if isinstance(ring, Equipment):
            self.equip(ring)
        if isinstance(amulet, Equipment):
            self.equip(amulet)

        self.__init = False

    def equip(
        self, new_equipment: Equipment, hand: str = None
    ) -> List[Equipment]:
        equip_type = new_equipment.equip_type
        requirements = new_equipment.requirements
        old_equipments = []
        errors = []
        if not self.__init:
            for attribute, value in requirements.items():
                if value > self.base_stats[attribute]:
                    errors.append(
                        f'    {attribute}: '
                        f'"{value}" ({self.base_stats[attribute]}).'
                    )

        if errors:
            errors = "\n".join(errors)
            raise EquipmentRequirementError(
                f'Não foi possível equipar o item "{new_equipment.name}".\n'
                'O personagem não possui os requisitos:\n'
                f'{errors}'
            )

        if equip_type == EquipmentEnum.HELMET:
            if self.helmet is not None:
                old_equipments.append(self.helmet)
            self.__helmet = new_equipment
        elif equip_type == EquipmentEnum.ONE_HAND:
            if not isinstance(hand, str):
                raise ValueError(
                    'É necessário indicar em qual das mãos o '
                    'item será equipado usando "LEFT" ou "RIGHT".\n'
                    f'Valor de hand, "{hand}", não é uma string.'
                )

            if self.equiped_two_handed_weapon():
                old_equipments.append(self.right_hand)
                self.__right_hand = None
                self.__left_hand = None

            if hand.upper() in ['R', 'RIGHT']:
                if self.right_hand is not None:
                    old_equipments.append(self.right_hand)
                self.__right_hand = new_equipment
            elif hand.upper() in ['L', 'LEFT']:
                if self.left_hand is not None:
                    old_equipments.append(self.left_hand)
                self.__left_hand = new_equipment
            else:
                raise ValueError(
                    f'Valor de hand, "{hand}", não é uma string válida. '
                    'Use LEFT ou RIGHT para a mão ESQUERDA ou DIREITA.'
                )

        elif equip_type == EquipmentEnum.TWO_HANDS:
            if self.equiped_two_handed_weapon():
                old_equipments.append(self.right_hand)
                self.__right_hand = None
                self.__left_hand = None

            if self.left_hand is not None:
                old_equipments.append(self.left_hand)
            if self.right_hand is not None:
                old_equipments.append(self.right_hand)
            self.__left_hand = new_equipment
            self.__right_hand = new_equipment
        elif equip_type == EquipmentEnum.ARMOR:
            if self.armor is not None:
                old_equipments.append(self.armor)
            self.__armor = new_equipment
        elif equip_type == EquipmentEnum.BOOTS:
            if self.boots is not None:
                old_equipments.append(self.boots)
            self.__boots = new_equipment
        elif equip_type == EquipmentEnum.RING:
            if self.ring is not None:
                old_equipments.append(self.ring)
            self.__ring = new_equipment
        elif equip_type == EquipmentEnum.AMULET:
            if self.amulet is not None:
                old_equipments.append(self.amulet)
            self.__amulet = new_equipment

        if not self.__init:
            self.notify_observers()

        return old_equipments

    def equiped_two_handed_weapon(self) -> bool:
        return (
            self.right_hand and
            self.right_hand.equip_type == EquipmentEnum.TWO_HANDS
        )

    def get_equipment_hands(self) -> List[Equipment]:
        weapons = []
        if self.equiped_two_handed_weapon():
            weapons.append(self.right_hand)
        else:
            weapons.extend([self.left_hand, self.right_hand])

        return [e for e in weapons if e is not None]

    def unequip(self, equipment: Equipment) -> Equipment:
        equip_type = equipment.equip_type

        if self.helmet == equipment:
            equipment = self.helmet
            self.__helmet = None
        elif self.left_hand == equipment:
            equipment = self.left_hand
            self.__left_hand = None
        elif self.right_hand == equipment:
            equipment = self.right_hand
            self.__right_hand = None
        elif self.armor == equipment:
            equipment = self.armor
            self.__armor = None
        elif self.boots == equipment:
            equipment = self.boots
            self.__boots = None
        elif self.ring == equipment:
            equipment = self.ring
            self.__ring = None
        elif self.amulet == equipment:
            equipment = self.amulet
            self.__amulet = None
        else:
            raise ValueError(f'"{equipment}" não está equipado.')

        if equip_type == EquipmentEnum.TWO_HANDS:
            self.__left_hand = None
            self.__right_hand = None

        self.notify_observers()
        return equipment

    def attach_observer(self, observer):
        self.__observers.append(observer)

    def detach_observer(self, observer):
        self.__observers.remove(observer)

    def notify_observers(self):
        for observer in self.__observers:
            observer.update()

    def get_attr_sum_from_equipments(self, attribute: str) -> int:
        value = sum([
            getattr(equipment, attribute)
            for equipment in self
        ])

        return int(value)

    def get_weight_sum_from_equipments(self, attribute: str) -> float:
        value = sum([
            getattr(equipment, attribute)
            for equipment in self
        ])

        return float(value)

    def get_multiplier_sum_from_equipments(self, attribute: str) -> float:
        value = 1.0 + sum([
            getattr(equipment, attribute) - 1.0
            for equipment in self
        ])

        return value

    def compare(self, equipment: Equipment, is_sell: bool = False) -> str:
        other_equipment = []
        if equipment.equip_type == EquipmentEnum.HELMET:
            other_equipment.append(self.helmet)
        elif equipment.equip_type == EquipmentEnum.ONE_HAND:
            other_equipment.append(self.right_hand)
        elif equipment.equip_type == EquipmentEnum.TWO_HANDS:
            equipment_hands = self.get_equipment_hands()
            other_equipment.extend(equipment_hands)
        elif equipment.equip_type == EquipmentEnum.ARMOR:
            other_equipment.append(self.armor)
        elif equipment.equip_type == EquipmentEnum.BOOTS:
            other_equipment.append(self.boots)
        elif equipment.equip_type == EquipmentEnum.RING:
            other_equipment.append(self.ring)
        elif equipment.equip_type == EquipmentEnum.AMULET:
            other_equipment.append(self.amulet)

        other_equipment = [e for e in other_equipment if e is not None]

        if not other_equipment:
            return equipment.get_sheet(
                verbose=True,
                markdown=True,
                is_sell=is_sell,
            )
        elif equipment.equip_type == EquipmentEnum.ONE_HAND and (
            self.left_hand is not None or self.right_hand is not None
        ):
            texts = []
            if (
                self.left_hand is not None and
                not self.equiped_two_handed_weapon()
            ):
                compare_text = equipment.compare(
                    self.left_hand,
                    is_sell=is_sell
                )
                texts.append(f'{EmojiEnum.LEFT.value}{compare_text}')
            if self.right_hand is not None:
                compare_text = equipment.compare(
                    self.right_hand,
                    is_sell=is_sell
                )
                texts.append(f'{EmojiEnum.RIGHT.value}{compare_text}')
            return f'\n{TEXT_SEPARATOR}\n\n'.join(texts)
        else:
            return equipment.compare(*other_equipment, is_sell=is_sell)

    def sheet_special_damages(self) -> str:
        special_damage_text = '\n'.join((
            f'  {special_damage.help_emoji_text}'
            for special_damage in self.special_damage_iter
        ))
        if special_damage_text:
            special_damage_text = f'*Dano Especial*:\n{special_damage_text}\n'
        special_damage_text += '\n'

        return special_damage_text

    def get_sheet(self, verbose: bool = False, markdown: bool = False) -> str:
        special_damages = self.sheet_special_damages()
        text = (
            f'*{SECTION_HEAD.format("EQUIPAMENTOS")}*\n'
            f'*Poder*: {self.power:}{EmojiEnum.EQUIPMENT_POWER.value}\n'
            f'*Peso*: {self.equipments_weight:.2f}{EmojiEnum.WEIGHT.value}\n'
            f'{special_damages}'

            '*Capacete*: '
            f'{self.helmet.name_power_level if self.helmet else ""}\n'
            '*Mão Esq.*: '
            f'{self.left_hand.name_power_level if self.left_hand else ""}\n'
            '*Mão Dir.*: '
            f'{self.right_hand.name_power_level if self.right_hand else ""}\n'
            '*Armadura*: '
            f'{self.armor.name_power_level if self.armor else ""}\n'
            '*Botas*: '
            f'{self.boots.name_power_level if self.boots else ""}\n'
            '*Anel*: '
            f'{self.ring.name_power_level if self.ring else ""}\n'
            '*Amuleto*: '
            f'{self.amulet.name_power_level if self.amulet else ""}\n\n'
        )

        if verbose:
            text += (
                f'*{SECTION_HEAD.format("BÔNUS E MULTIPLICADORES")}*\n'

                f'`{STRENGTH_EMOJI_TEXT}: {self.strength:+} '
                f'x({self.multiplier_strength:+.2f})`\n'
                f'`{DEXTERITY_EMOJI_TEXT}: {self.dexterity:+} '
                f'x({self.multiplier_dexterity:+.2f})`\n'
                f'`{CONSTITUTION_EMOJI_TEXT}: {self.constitution:+} '
                f'x({self.multiplier_constitution:+.2f})`\n'
                f'`{INTELLIGENCE_EMOJI_TEXT}: {self.intelligence:+} '
                f'x({self.multiplier_intelligence:+.2f})`\n'
                f'`{WISDOM_EMOJI_TEXT}: {self.wisdom:+} '
                f'x({self.multiplier_wisdom:+.2f})`\n'
                f'`{CHARISMA_EMOJI_TEXT}: {self.charisma:+} '
                f'x({self.multiplier_charisma:+.2f})`\n\n'

                f'`{HIT_POINT_FULL_EMOJI_TEXT}: {self.hp:+}`\n'
                f'`{INITIATIVE_EMOJI_TEXT}: {self.initiative:+}`\n'
                f'`{PHYSICAL_ATTACK_EMOJI_TEXT}: {self.physical_attack:+}`\n'
                f'`{PRECISION_ATTACK_EMOJI_TEXT}: {self.precision_attack:+}`\n'
                f'`{MAGICAL_ATTACK_EMOJI_TEXT}: {self.magical_attack:+}`\n'
                f'`{PHYSICAL_DEFENSE_EMOJI_TEXT}: {self.physical_defense:+}`\n'
                f'`{MAGICAL_DEFENSE_EMOJI_TEXT}: {self.magical_defense:+}`\n'
                f'`{HIT_EMOJI_TEXT}: {self.hit:+}`\n'
                f'`{EVASION_EMOJI_TEXT}: {self.evasion:+}`\n'
            )

        if not markdown:
            text = remove_bold(text)
            text = remove_code(text)
        else:
            text = escape_basic_markdown_v2(text)

        return text

    def get_all_sheets(
        self, verbose: bool = False, markdown: bool = False
    ) -> str:
        return self.get_sheet(verbose=verbose, markdown=markdown)

    def __repr__(self) -> str:
        return (
            f'{TEXT_DELIMITER}\n'
            f'{self.get_sheet(True)}'
            f'{TEXT_DELIMITER}'
        )

    def to_dict(self):
        return dict(
            player_id=self.__player_id,
            _id=self.__id,
            helmet_id=self.helmet._id if self.helmet else None,
            left_hand_id=self.left_hand._id if self.left_hand else None,
            right_hand_id=self.right_hand._id if self.right_hand else None,
            armor_id=self.armor._id if self.armor else None,
            boots_id=self.boots._id if self.boots else None,
            ring_id=self.ring._id if self.ring else None,
            amulet_id=self.amulet._id if self.amulet else None,
            # observers=[o._id for o in self.__observers],
            created_at=self.__created_at,
            updated_at=self.__updated_at,
        )

    def __iter__(self) -> Iterable[Equipment]:
        equips = [
            self.helmet, self.left_hand, self.right_hand,
            self.armor, self.boots, self.ring, self.amulet
        ]
        if self.equiped_two_handed_weapon():
            equips.remove(self.right_hand)

        for equip in equips:
            if equip:
                yield equip

    # Getters
    @property
    def base_stats(self):
        for observer in self.__observers:
            if isinstance(observer, BaseStats):
                return observer
        raise NameError('Não foi encontrado um observer do tipo BaseStats.')

    @property
    def power(self):
        power = 0
        for equip in self:
            power += equip.power

        return power

    @property
    def special_damage_iter(self) -> Iterator[SpecialDamage]:
        hand_equipments = self.get_equipment_hands()
        special_damages_dict = {}
        special_damages_gen = (
            special_damage
            for equipment in hand_equipments
            for special_damage in equipment.special_damage_iter
        )

        for special_damage in special_damages_gen:
            damage_type = special_damage.damage_type
            base_damage = special_damage.base_damage
            equip_level = special_damage.equipment_level
            damage_dict = special_damages_dict.setdefault(damage_type, {})
            damage_dict.setdefault('base_damage', []).append(base_damage)
            damage_dict.setdefault('equipment_level', []).append(equip_level)
            damage_dict.setdefault('status_multiplier', []).append(1)

        for damage_type, damage_dict in special_damages_dict.items():
            base_damage = sum(damage_dict['base_damage'])
            status_multiplier = sum(damage_dict['status_multiplier'])
            equipment_level = mean(damage_dict['equipment_level'])
            if base_damage > 0:
                yield SpecialDamage(
                    base_damage=base_damage,
                    damage_type=damage_type,
                    equipment_level=equipment_level,
                    status_multiplier=status_multiplier,
                )

    _id = property(lambda self: self.__id)
    helmet = property(lambda self: self.__helmet)
    left_hand = property(lambda self: self.__left_hand)
    right_hand = property(lambda self: self.__right_hand)
    armor = property(lambda self: self.__armor)
    boots = property(lambda self: self.__boots)
    ring = property(lambda self: self.__ring)
    amulet = property(lambda self: self.__amulet)

    @property
    def equipments_weight(self) -> int:
        return self.get_weight_sum_from_equipments('weight')

    @property
    def bonus_strength(self) -> int:
        return self.get_attr_sum_from_equipments('bonus_strength')

    @property
    def bonus_dexterity(self) -> int:
        return self.get_attr_sum_from_equipments('bonus_dexterity')

    @property
    def bonus_constitution(self) -> int:
        return self.get_attr_sum_from_equipments('bonus_constitution')

    @property
    def bonus_intelligence(self) -> int:
        return self.get_attr_sum_from_equipments('bonus_intelligence')

    @property
    def bonus_wisdom(self) -> int:
        return self.get_attr_sum_from_equipments('bonus_wisdom')

    @property
    def bonus_charisma(self) -> int:
        return self.get_attr_sum_from_equipments('bonus_charisma')

    @property
    def multiplier_strength(self) -> float:
        return self.get_multiplier_sum_from_equipments(
            'multiplier_strength'
        )

    @property
    def multiplier_dexterity(self) -> float:
        return self.get_multiplier_sum_from_equipments(
            'multiplier_dexterity'
        )

    @property
    def multiplier_constitution(self) -> float:
        return self.get_multiplier_sum_from_equipments(
            'multiplier_constitution'
        )

    @property
    def multiplier_intelligence(self) -> float:
        return self.get_multiplier_sum_from_equipments(
            'multiplier_intelligence'
        )

    @property
    def multiplier_wisdom(self) -> float:
        return self.get_multiplier_sum_from_equipments(
            'multiplier_wisdom'
        )

    @property
    def multiplier_charisma(self) -> float:
        return self.get_multiplier_sum_from_equipments(
            'multiplier_charisma'
        )

    @property
    def bonus_hit_points(self) -> int:
        return self.get_attr_sum_from_equipments('bonus_hit_points')

    @property
    def bonus_initiative(self) -> int:
        return self.get_attr_sum_from_equipments('bonus_initiative')

    @property
    def bonus_physical_attack(self) -> int:
        return self.get_attr_sum_from_equipments('bonus_physical_attack')

    @property
    def bonus_precision_attack(self) -> int:
        return self.get_attr_sum_from_equipments('bonus_precision_attack')

    @property
    def bonus_magical_attack(self) -> int:
        return self.get_attr_sum_from_equipments('bonus_magical_attack')

    @property
    def bonus_physical_defense(self) -> int:
        return self.get_attr_sum_from_equipments('bonus_physical_defense')

    @property
    def bonus_magical_defense(self) -> int:
        return self.get_attr_sum_from_equipments('bonus_magical_defense')

    @property
    def bonus_hit(self) -> int:
        return self.get_attr_sum_from_equipments('bonus_hit')

    @property
    def bonus_evasion(self) -> int:
        return self.get_attr_sum_from_equipments('bonus_evasion')

    strength = bonus_strength
    dexterity = bonus_dexterity
    constitution = bonus_constitution
    intelligence = bonus_intelligence
    wisdom = bonus_wisdom
    charisma = bonus_charisma
    hp = hit_points = bonus_hit_points
    initiative = bonus_initiative
    physical_attack = bonus_physical_attack
    precision_attack = bonus_precision_attack
    magical_attack = bonus_magical_attack
    physical_defense = bonus_physical_defense
    magical_defense = bonus_magical_defense
    hit = bonus_hit
    evasion = bonus_evasion


if __name__ == '__main__':
    helmet = Equipment(
        name='Capacete de Aço',
        equip_type=EquipmentEnum.HELMET,
        damage_types=None,
        weight=10,
        requirements={'level': 10},
        bonus_physical_defense=30,
        bonus_evasion=-5,
    )
    sword = Equipment(
        name='Espada Gigante de Aço',
        equip_type=EquipmentEnum.TWO_HANDS,
        damage_types=DamageEnum.SLASHING,
        weight=40,
        bonus_physical_attack=60,
        bonus_hit=15,
        bonus_evasion=-20,
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
    any_ring = Equipment(
        name='Algum Anel',
        equip_type=EquipmentEnum.RING,
        damage_types=None,
        weight=0.1,
        bonus_strength=100,
        bonus_dexterity=100,
        bonus_constitution=100,
        bonus_intelligence=100,
        bonus_wisdom=100,
        bonus_charisma=100,
        multiplier_strength=2,
        multiplier_dexterity=2,
        multiplier_constitution=2,
        multiplier_intelligence=2,
        multiplier_wisdom=2,
        multiplier_charisma=2,
        bonus_hit_points=1000,
        bonus_initiative=100,
        bonus_physical_attack=100,
        bonus_precision_attack=100,
        bonus_magical_attack=100,
        bonus_physical_defense=100,
        bonus_magical_defense=-100,
        bonus_hit=100,
        bonus_evasion=100,
    )
    amulet = Equipment(
        name='Colar Brilhante',
        equip_type=EquipmentEnum.AMULET,
        damage_types=None,
        weight=0.2,
        bonus_charisma=150,
    )
    dagger = Equipment(
        name='Adaga de Aço',
        equip_type=EquipmentEnum.ONE_HAND,
        damage_types=DamageEnum.SLASHING,
        weight=40,
        bonus_physical_attack=30,
        bonus_hit=15,
        bonus_evasion=-10,
    )
    shield = Equipment(
        name='Escudo de Aço',
        equip_type=EquipmentEnum.ONE_HAND,
        damage_types=DamageEnum.BLUDGEONING,
        weight=40,
        bonus_physical_defense=30,
        bonus_hit=15,
        bonus_evasion=-10,
    )

    equips = Equips(player_id=123, helmet=helmet)
    equips.equip(sword)
    equips.equip(shield, 'LEFT')
    equips.equip(dagger, 'RIGHT')
    equips.equip(armor)
    equips.equip(boots)
    equips.equip(any_ring)
    equips.equip(amulet)
    print(equips.compare(sword))
    print(equips.get_sheet(True))
    print(equips.to_dict())

    # Verificar se estar retornando os equipamentos certos
    # ao trocar de equipamentos
    result = equips.equip(sword)
    if shield in result and dagger in result:
        print(
            f'Equipou {sword.name} e '
            f'recebeu {result[0].name} e {result[1].name}.'
        )
    else:
        raise Exception(
            'Deveria receber dois equipamentos (shield e dagger), '
            f'mas rebebeu {result}.'
        )
    result = equips.equip(sword)
    if sword in result:
        print(
            f'Equipou {sword.name} e '
            f'recebeu {result[0].name}.'
        )
    else:
        raise Exception(
            f'Deveria receber um equipamento (sword), mas rebebeu {result}.'
        )
