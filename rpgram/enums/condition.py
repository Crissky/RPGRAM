from enum import Enum


class ConditionEnum(Enum):
    BLEEDING = 'Sangramento'
    BLINDNESS = 'Cegueira'
    BURN = 'Queimadura'
    CONFUSION = 'Confusão'
    CURSE = 'Maldição'
    EXHAUSTION = 'Exaustão'
    FROZEN = 'Congelado'
    PARALYSIS = 'Paralisia'
    PETRIFIED = 'Petrificado'
    POISONING = 'Envenenamento'
    SILENCE = 'Silêncio'


BLEEDING = ConditionEnum.BLEEDING.name.title()
BLINDNESS = ConditionEnum.BLINDNESS.name.title()
BURN = ConditionEnum.BURN.name.title()
CONFUSION = ConditionEnum.CONFUSION.name.title()
CURSE = ConditionEnum.CURSE.name.title()
EXHAUSTION = ConditionEnum.EXHAUSTION.name.title()
FROZEN = ConditionEnum.FROZEN.name.title()
PARALYSIS = ConditionEnum.PARALYSIS.name.title()
PETRIFIED = ConditionEnum.PETRIFIED.name.title()
POISONING = ConditionEnum.POISONING.name.title()
SILENCE = ConditionEnum.SILENCE.name.title()
