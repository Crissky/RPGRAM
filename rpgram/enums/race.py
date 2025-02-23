from enum import Enum


class RaceEnum(Enum):
    DWARF = 'Anão'
    ELF = 'Elfo'
    HALFLING = 'Halfling'
    HUMAN = 'Humano'
    ORC = 'Orque'
    DROW = 'Drow'
    GOBLIN = 'Goblin'
    TROLL = 'Troll'
    KOBOLD = 'Kobold'
    SPECTRUM = 'Espectro'
    OGRE = 'Ogro'
    LYCANTHROPE = 'Licantropo'
    HARPY = 'Harpia'
    LAMIA = 'Lâmia'
    DRACONIAN = 'Draconiano'
    DRYAD = 'Dríade'
    SYLPH = 'Sílfide'
    GNOLL = 'Gnoll'
    FOMORI = 'Fomori'
    NEPHILIM = 'Nefilim'


MALEGNE_RACES = [
    RaceEnum.SPECTRUM.value,
    RaceEnum.FOMORI.value,
    RaceEnum.NEPHILIM.value,
]
TRANSGRESSOR_RACES = [
    RaceEnum.ORC.value,
    RaceEnum.DROW.value,
    RaceEnum.GOBLIN.value,
    RaceEnum.TROLL.value,
    RaceEnum.KOBOLD.value,
    RaceEnum.SPECTRUM.value,
    RaceEnum.OGRE.value,
    RaceEnum.LYCANTHROPE.value,
    RaceEnum.HARPY.value,
    RaceEnum.LAMIA.value,
    RaceEnum.GNOLL.value,
    RaceEnum.FOMORI.value,
    RaceEnum.NEPHILIM.value,
]
