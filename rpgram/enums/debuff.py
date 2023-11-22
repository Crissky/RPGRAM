from enum import Enum


class DebuffEnum(Enum):
    BLEEDING = 'Sangrando'
    BLINDNESS = 'Cego'
    BURN = 'Afogueado'
    CONFUSION = 'Confuso'
    CURSE = 'Amaldiçoado'
    EXHAUSTION = 'Exausto'
    FROZEN = 'Congelado'
    PARALYSIS = 'Paralisado'
    PETRIFIED = 'Petrificado'
    POISONING = 'Envenenado'
    SILENCE = 'Silenciado'


class DebuffEmojiEnum(Enum):
    BLEEDING = '🩸'
    BLINDNESS = '🕶️'
    BURN = '🔥'
    CONFUSION = '🌀'
    CURSE = '🎃'
    EXHAUSTION = '💧'
    FROZEN = '❄️'
    PARALYSIS = '♒︎'
    PETRIFIED = '🪨'
    POISONING = '🍄'
    SILENCE = '💬'


DEBUFF_FULL_NAMES = {
    debuff.name: DebuffEmojiEnum[debuff.name].value + debuff.value
    for debuff in DebuffEnum
}

BLEEDING = DebuffEnum.BLEEDING.name.title()
BLINDNESS = DebuffEnum.BLINDNESS.name.title()
BURN = DebuffEnum.BURN.name.title()
CONFUSION = DebuffEnum.CONFUSION.name.title()
CURSE = DebuffEnum.CURSE.name.title()
EXHAUSTION = DebuffEnum.EXHAUSTION.name.title()
FROZEN = DebuffEnum.FROZEN.name.title()
PARALYSIS = DebuffEnum.PARALYSIS.name.title()
PETRIFIED = DebuffEnum.PETRIFIED.name.title()
POISONING = DebuffEnum.POISONING.name.title()
SILENCE = DebuffEnum.SILENCE.name.title()
