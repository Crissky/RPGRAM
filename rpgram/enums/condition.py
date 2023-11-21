from enum import Enum


class DebuffEnum(Enum):
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
