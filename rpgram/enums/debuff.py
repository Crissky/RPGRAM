from enum import Enum
from rpgram.enums.skill import BarbarianSkillEnum
from typing import Union


class DebuffEnum(Enum):
    BERSERKER = 'Berserker'
    BLEEDING = 'Sangrando'
    BLINDNESS = 'Cego'
    BURN = 'Afogueado'
    CONFUSION = 'Confuso'
    CRYSTALLIZED = 'Cristalizado'
    CURSE = 'Amaldiçoado'
    DEATH_SENTENCE = 'Sentença de Morte'
    EXHAUSTION = 'Exausto'
    FEARING = 'Amedrontado'
    FROZEN = 'Congelado'
    IMPRISONED = 'Aprisionado'
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
    DEATH_SENTENCE = '🪦'
    FEARING = '😰'
    FROZEN = '🥶'
    IMPRISONED = '🪢'
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
    DebuffEnum.IMPRISONED.name,
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


def get_debuff_emoji_text(debuff_name: Union[DebuffEnum, str]) -> str:
    '''Retorna string com o emoji e o nome do debuff.
    '''

    if isinstance(debuff_name, str):
        debuff_name = DebuffEnum[debuff_name]
    name = debuff_name.name

    return f'{DebuffEmojiEnum[name].value}{name.title()}'


def get_debuffs_emoji_text(
    *debuff_names: Union[DebuffEnum, str],
    sep: str = ', '
) -> str:
    '''Retorna tupla de debuffs como uma string com o emoji e 
    o nome do debuff separados pelo "sep".
    '''

    return sep.join([get_debuff_emoji_text(d) for d in debuff_names])


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
