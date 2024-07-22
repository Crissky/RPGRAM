from rpgram.enums.skill import BarbarianSkillEnum
from enum import Enum
from typing import Union


class DebuffEnum(Enum):
    BERSERKER = 'Berserker'
    BLEEDING = 'Sangrando'
    BLINDNESS = 'Cego'
    BURN = 'Afogueado'
    CONFUSION = 'Confuso'
    CRYSTALLIZED = 'Cristalizado'
    CURSE = 'Amaldiçoado'
    EXHAUSTION = 'Exausto'
    FEARING = 'Medo'
    FROZEN = 'Congelado'
    PARALYSIS = 'Paralisado'
    PETRIFIED = 'Petrificado'
    POISONING = 'Envenenado'
    SILENCE = 'Silenciado'
    STUNNED = 'Atordoado'


class DebuffEmojiEnum(Enum):
    BERSERKER = '💢'
    BLEEDING = '🩸'
    BLINDNESS = '🕶️'
    BURN = '❤️‍🔥'  # 🔥
    CONFUSION = '🌀'
    CRYSTALLIZED = '🧊'
    CURSE = '🎃'
    EXHAUSTION = '💧'
    FEARING = '😰'
    FROZEN = '🥶'
    PARALYSIS = '♒︎'
    PETRIFIED = '🗿'  # 🪨
    POISONING = '🍄'
    SILENCE = '💬'
    STUNNED = '🎇'  # ❇️


DEBUFF_FULL_NAMES = {
    debuff.name: DebuffEmojiEnum[debuff.name].value + debuff.value
    for debuff in DebuffEnum
}


CURSED_DEBUFFS_NAMES = [
    DebuffEnum.CURSE.name,
]
CONFUSION_DEBUFFS_NAMES = [
    DebuffEnum.BERSERKER.name,
    DebuffEnum.CONFUSION.name,
    BarbarianSkillEnum.FRENZY.name,
]
IMMOBILIZED_DEBUFFS_NAMES = [
    DebuffEnum.CRYSTALLIZED.name,
    DebuffEnum.FEARING.name,
    DebuffEnum.FROZEN.name,
    DebuffEnum.PARALYSIS.name,
    DebuffEnum.PETRIFIED.name,
    DebuffEnum.STUNNED.name,
]
SILENCED_DEBUFFS_NAMES = [DebuffEnum.SILENCE.name]
BREAKABLE_IMMOBILIZED_DEBUFFS_NAMES = [
    DebuffEnum.CRYSTALLIZED.name,
    DebuffEnum.FROZEN.name,
    DebuffEnum.PETRIFIED.name,
]


def get_debuff_emoji_text(damage: Union[DebuffEnum, str]) -> str:
    if isinstance(damage, str):
        damage = DebuffEnum[damage]
    name = damage.name

    return f'{DebuffEmojiEnum[name].value}{name.title()}'


if __name__ == '__main__':
    debuff_name_list = [debuff.name for debuff in DebuffEnum]
    debuff_emoji_name_list = [
        debuff_emoji.name
        for debuff_emoji in DebuffEmojiEnum
    ]

    for debuff_name in debuff_name_list:
        if debuff_name not in debuff_emoji_name_list:
            raise ValueError(
                f'{debuff_name} não está em {DebuffEmojiEnum.__name__}.')

    for debuff_emoji_name in debuff_emoji_name_list:
        if debuff_emoji_name not in debuff_name_list:
            raise ValueError(
                f'{debuff_emoji_name} não está em {DebuffEnum.__name__}.'
            )

    print('Debuffs OK!')
