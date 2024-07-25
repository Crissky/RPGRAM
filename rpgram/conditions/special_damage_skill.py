from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Iterable, Iterator, List, Union

from bson import ObjectId

from rpgram.conditions.buff import BuffCondition
from rpgram.enums.damage import (
    DamageEmojiEnum,
    DamageEnum
)
from rpgram.enums.skill import (
    BarbarianSkillEnum,
    DruidSkillEnum,
    GuardianSkillEnum
)
from rpgram.enums.turn import TurnEnum
from rpgram.skills.special_damage import SpecialDamage


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class SpecialDamageSkillCondition(BuffCondition):

    def __init__(
        self,
        name: Enum,
        frequency: Union[str, TurnEnum],
        power: int,
        damage_types: List[Union[str, DamageEnum]],
        turn: int = 1,
        level: int = 1,
        _id: Union[str, ObjectId] = None,
        created_at: datetime = None,
        updated_at: datetime = None,
    ):
        super().__init__(
            name=name,
            frequency=frequency,
            turn=turn,
            level=level,
            _id=_id,
            created_at=created_at,
            updated_at=updated_at,
        )

        if isinstance(damage_types, (DamageEnum, str)):
            damage_types = [damage_types]
        for index, damage_type in enumerate(damage_types):
            if isinstance(damage_type, str):
                damage_type = DamageEnum[damage_type]
            if isinstance(damage_type, DamageEnum):
                damage_types[index] = damage_type
            else:
                raise ValueError(
                    f'damage_types precisa ser uma string ou DamageEnum ou '
                    f'uma lista de strings ou DamageEnums. '
                    f'"{type(damage_type)}" não é válido.'
                )

        self._power = int(power)
        self.damage_types = damage_types

    @property
    def power(self) -> int:
        power_multiplier = 1 + (self.level / 10)
        power_multiplier = round(power_multiplier, 2)

        return int(self._power * power_multiplier)

    @property
    def emoji(self) -> str:
        return '🔷'

    @property
    def damage_emoji_name(self) -> str:
        return ', '.join([
            damage.damage_emoji_name
            for damage in self.special_damage_iter
        ])

    @property
    def damage_full_text(self) -> str:
        return ', '.join([
            damage.damage_full_text
            for damage in self.special_damage_iter
        ])

    @property
    def damage_help_emoji_text(self) -> str:
        return ', '.join([
            damage.damage_help_emoji_text
            for damage in self.special_damage_iter
        ])

    @property
    def special_damage_iter(self) -> Iterator[SpecialDamage]:
        # Mesmo valor de condition_reducer em SpecialDamage
        condition_multiplier = 20
        base_damage = self.power
        for damage_type in self.damage_types:
            if base_damage > 0:
                yield SpecialDamage(
                    base_damage=base_damage,
                    damage_type=damage_type,
                    equipment_level=int(self.level * condition_multiplier),
                    is_skill=True
                )
            else:
                break

    def function(self, target: 'BaseCharacter') -> dict:
        report = {'text': '', 'action': self.name}
        if self.turn != 1:
            text = (
                f'*{self.full_name}*: '
                f'*{target.name}* está imbuído com a *{self.name}*.'
            )
            report['text'] = text

        return report

    def to_dict(self) -> dict:
        _dict = {'power': self._power}
        _dict.update(super().to_dict())

        return _dict


class SDCrystallineInfusionCondition(SpecialDamageSkillCondition):

    def __init__(
        self,
        power: int,
        turn: int = 10,
        level: int = 1,
    ):
        super().__init__(
            name=GuardianSkillEnum.CRYSTALLINE_INFUSION,
            frequency=TurnEnum.START,
            power=power,
            damage_types=[DamageEnum.CRYSTAL],
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'Infusão de *Cristais Místicos* que '
            f'concede dano de {self.damage_help_emoji_text}.'
        )

    @property
    def emoji(self) -> str:
        return DamageEmojiEnum.CRYSTAL.value


class SDWildFireCondition(SpecialDamageSkillCondition):

    def __init__(
        self,
        power: int,
        turn: int = 10,
        level: int = 1,
    ):
        super().__init__(
            name=BarbarianSkillEnum.WILD_FIRE,
            frequency=TurnEnum.START,
            power=power,
            damage_types=[DamageEnum.FIRE],
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*Infusão Selvagem* que '
            f'concede dano de {self.damage_help_emoji_text}.'
        )

    @property
    def emoji(self) -> str:
        return DamageEmojiEnum.FIRE.value


class SDWildLightningCondition(SpecialDamageSkillCondition):

    def __init__(
        self,
        power: int,
        turn: int = 10,
        level: int = 1,
    ):
        super().__init__(
            name=BarbarianSkillEnum.WILD_LIGHTNING,
            frequency=TurnEnum.START,
            power=power,
            damage_types=[DamageEnum.LIGHTNING],
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*Infusão Selvagem* que '
            f'concede dano de {self.damage_help_emoji_text}.'
        )

    @property
    def emoji(self) -> str:
        return DamageEmojiEnum.LIGHTNING.value


class SDWildWindCondition(SpecialDamageSkillCondition):

    def __init__(
        self,
        power: int,
        turn: int = 10,
        level: int = 1,
    ):
        super().__init__(
            name=BarbarianSkillEnum.WILD_WIND,
            frequency=TurnEnum.START,
            power=power,
            damage_types=[DamageEnum.WIND],
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*Infusão Selvagem* que '
            f'concede dano de {self.damage_help_emoji_text}.'
        )

    @property
    def emoji(self) -> str:
        return DamageEmojiEnum.WIND.value


class SDWildRockCondition(SpecialDamageSkillCondition):

    def __init__(
        self,
        power: int,
        turn: int = 10,
        level: int = 1,
    ):
        super().__init__(
            name=BarbarianSkillEnum.WILD_ROCK,
            frequency=TurnEnum.START,
            power=power,
            damage_types=[DamageEnum.ROCK],
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*Infusão Selvagem* que '
            f'concede dano de {self.damage_help_emoji_text}.'
        )

    @property
    def emoji(self) -> str:
        return DamageEmojiEnum.ROCK.value


class SDWildGroundCondition(SpecialDamageSkillCondition):

    def __init__(
        self,
        power: int,
        turn: int = 10,
        level: int = 1,
    ):
        super().__init__(
            name=BarbarianSkillEnum.WILD_GROUND,
            frequency=TurnEnum.START,
            power=power,
            damage_types=[DamageEnum.GROUND],
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*Infusão Selvagem* que '
            f'concede dano de {self.damage_help_emoji_text}.'
        )

    @property
    def emoji(self) -> str:
        return DamageEmojiEnum.GROUND.value


class SDWildAcidCondition(SpecialDamageSkillCondition):

    def __init__(
        self,
        power: int,
        turn: int = 10,
        level: int = 1,
    ):
        super().__init__(
            name=BarbarianSkillEnum.WILD_ACID,
            frequency=TurnEnum.START,
            power=power,
            damage_types=[DamageEnum.ACID],
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*Infusão Selvagem* que '
            f'concede dano de {self.damage_help_emoji_text}.'
        )

    @property
    def emoji(self) -> str:
        return DamageEmojiEnum.ACID.value


class SDWildPoisonCondition(SpecialDamageSkillCondition):

    def __init__(
        self,
        power: int,
        turn: int = 10,
        level: int = 1,
    ):
        super().__init__(
            name=BarbarianSkillEnum.WILD_POISON,
            frequency=TurnEnum.START,
            power=power,
            damage_types=[DamageEnum.POISON],
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*Infusão Selvagem* que '
            f'concede dano de {self.damage_help_emoji_text}.'
        )

    @property
    def emoji(self) -> str:
        return DamageEmojiEnum.POISON.value


class SDFellowFalconCondition(SpecialDamageSkillCondition):

    def __init__(
        self,
        power: int,
        turn: int = 10,
        level: int = 1,
    ):
        super().__init__(
            name=DruidSkillEnum.FELLOW_FALCON,
            frequency=TurnEnum.START,
            power=power,
            damage_types=[DamageEnum.PIERCING, DamageEnum.FIRE],
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*{self.enum_name.value}* que o ajuda em batalha, '
            f'concedendo dano de {self.damage_help_emoji_text}.'
        )

    @property
    def emoji(self) -> str:
        return '🗡🦅'

    def function(self, target: 'BaseCharacter') -> dict:
        report = {'text': '', 'action': self.name}
        if self.turn != 1:
            text = (
                f'*{self.full_name}*: '
                f'*{target.name}* '
                f'permanece lutando ao lado do *{self.enum_name.value}*.'
            )
            report['text'] = text

        return report


class SDFellowBearCondition(SpecialDamageSkillCondition):

    def __init__(
        self,
        power: int,
        turn: int = 10,
        level: int = 1,
    ):
        super().__init__(
            name=DruidSkillEnum.FELLOW_BEAR,
            frequency=TurnEnum.START,
            power=power,
            damage_types=[DamageEnum.BLUDGEONING, DamageEnum.GROUND],
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*{self.enum_name.value}* que o ajuda em batalha, '
            f'concedendo dano de {self.damage_help_emoji_text}.'
        )

    @property
    def emoji(self) -> str:
        return '🗡🐻'

    def function(self, target: 'BaseCharacter') -> dict:
        report = {'text': '', 'action': self.name}
        if self.turn != 1:
            text = (
                f'*{self.full_name}*: '
                f'*{target.name}* '
                f'permanece lutando ao lado do *{self.enum_name.value}*.'
            )
            report['text'] = text

        return report


class SDFellowTigerCondition(SpecialDamageSkillCondition):

    def __init__(
        self,
        power: int,
        turn: int = 10,
        level: int = 1,
    ):
        super().__init__(
            name=DruidSkillEnum.FELLOW_TIGER,
            frequency=TurnEnum.START,
            power=power,
            damage_types=[DamageEnum.SLASHING, DamageEnum.LIGHTNING],
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*{self.enum_name.value}* que o ajuda em batalha, '
            f'concedendo dano de {self.damage_help_emoji_text}.'
        )

    @property
    def emoji(self) -> str:
        return '🗡🐯'

    def function(self, target: 'BaseCharacter') -> dict:
        report = {'text': '', 'action': self.name}
        if self.turn != 1:
            text = (
                f'*{self.full_name}*: '
                f'*{target.name}* '
                f'permanece lutando ao lado do *{self.enum_name.value}*.'
            )
            report['text'] = text

        return report


class SDFellowOwlCondition(SpecialDamageSkillCondition):

    def __init__(
        self,
        power: int,
        turn: int = 10,
        level: int = 1,
    ):
        super().__init__(
            name=DruidSkillEnum.FELLOW_OWL,
            frequency=TurnEnum.START,
            power=power,
            damage_types=[DamageEnum.MAGIC, DamageEnum.WIND],
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*{self.enum_name.value}* que o ajuda em batalha, '
            f'concedendo dano de {self.damage_help_emoji_text}.'
        )

    @property
    def emoji(self) -> str:
        return '🗡🦉'

    def function(self, target: 'BaseCharacter') -> dict:
        report = {'text': '', 'action': self.name}
        if self.turn != 1:
            text = (
                f'*{self.full_name}*: '
                f'*{target.name}* '
                f'permanece lutando ao lado da *{self.enum_name.value}*.'
            )
            report['text'] = text

        return report


class SDVineThornySpaulderCondition(SpecialDamageSkillCondition):

    def __init__(
        self,
        power: int,
        turn: int = 10,
        level: int = 1,
    ):
        super().__init__(
            name=DruidSkillEnum.VINE_THORNY_SPAULDER,
            frequency=TurnEnum.START,
            power=power,
            damage_types=[DamageEnum.PIERCING],
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*{self.enum_name.value}* que '
            f'concede dano de {self.damage_help_emoji_text}.'
        )

    @property
    def emoji(self) -> str:
        return '🗡🍇'

    def function(self, target: 'BaseCharacter') -> dict:
        report = {'text': '', 'action': self.name}
        if self.turn != 1:
            text = (
                f'*{self.full_name}*: '
                f'*{target.name}* '
                f'permanece equipado com a *{self.enum_name.value}*.'
            )
            report['text'] = text

        return report


class SDPoisonousSapCondition(SpecialDamageSkillCondition):

    def __init__(
        self,
        power: int,
        turn: int = 10,
        level: int = 1,
    ):
        super().__init__(
            name=DruidSkillEnum.POISONOUS_SAP,
            frequency=TurnEnum.START,
            power=power,
            damage_types=[DamageEnum.POISON],
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*{self.enum_name.value}* que '
            f'concede dano de {self.damage_help_emoji_text}.'
        )

    @property
    def emoji(self) -> str:
        return DamageEmojiEnum.POISON.value + '🍯'


class SpecialDamageBuffs:
    __list = [
        SDCrystallineInfusionCondition,
        SDWildFireCondition,
        SDWildLightningCondition,
        SDWildWindCondition,
        SDWildRockCondition,
        SDWildGroundCondition,
        SDWildAcidCondition,
        SDWildPoisonCondition,
        SDFellowFalconCondition,
        SDFellowBearCondition,
        SDFellowTigerCondition,
        SDFellowOwlCondition,
        SDVineThornySpaulderCondition,
        SDPoisonousSapCondition,
    ]

    def __iter__(self) -> Iterable[SpecialDamageSkillCondition]:
        for condition_class in self.__list:
            yield condition_class(power=100)


SPECIAL_DAMAGE_BUFFS: Iterable[SpecialDamageSkillCondition] = (
    SpecialDamageBuffs()
)


if __name__ == '__main__':
    from rpgram.conditions.factory import condition_factory

    for condition in SpecialDamageBuffs():
        print(condition)
        print(condition.to_dict())
        assert condition_factory(**condition.to_dict()) == condition
