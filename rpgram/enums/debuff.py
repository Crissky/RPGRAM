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


BERSERKER = DebuffEnum.BERSERKER.name.title()
BLEEDING = DebuffEnum.BLEEDING.name.title()
BLINDNESS = DebuffEnum.BLINDNESS.name.title()
BURN = DebuffEnum.BURN.name.title()
CONFUSION = DebuffEnum.CONFUSION.name.title()
CRYSTALLIZED = DebuffEnum.CRYSTALLIZED.name.title()
CURSE = DebuffEnum.CURSE.name.title()
EXHAUSTION = DebuffEnum.EXHAUSTION.name.title()
FEARING = DebuffEnum.FEARING.name.title()
FROZEN = DebuffEnum.FROZEN.name.title()
PARALYSIS = DebuffEnum.PARALYSIS.name.title()
PETRIFIED = DebuffEnum.PETRIFIED.name.title()
POISONING = DebuffEnum.POISONING.name.title()
SILENCE = DebuffEnum.SILENCE.name.title()
STUNNED = DebuffEnum.STUNNED.name.title()

FRENZY = BarbarianSkillEnum.FRENZY.value


CONFUSION_DEBUFFS_NAMES = [BERSERKER, CONFUSION, FRENZY]
IMMOBILIZED_DEBUFFS_NAMES = [
    CRYSTALLIZED, FROZEN, PARALYSIS, PETRIFIED, STUNNED, FEARING
]
SILENCED_DEBUFFS_NAMES = [SILENCE]
BREAKABLE_IMMOBILIZED_DEBUFFS_NAMES = [CRYSTALLIZED, FROZEN, PETRIFIED]


def get_debuff_emoji_text(damage: Union[DebuffEnum, str]) -> str:
    if isinstance(damage, str):
        damage = DebuffEnum[damage]
    name = damage.name
    return f'{DebuffEmojiEnum[name].value}{damage.name.title()}'


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
