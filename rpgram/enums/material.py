from enum import Enum


class WeaponMaterialEnum(Enum):
    WOOD = 'Madeira'
    BONE = 'Osso'
    COPPER = 'Cobre'
    IRON = 'Ferro'
    STEEL = 'Aço'
    OBSIDIAN = 'Obsidiana'
    RUNITE = 'Runita'
    ADAMANTIUM = 'Adamantium'
    MITHRIL = 'Mitril'


class MagicalQuillMaterialEnum(Enum):
    YATAGARASU = 'Corvo-de-Três-Pernas'
    HARPIA = 'Harpia'
    ROC = 'Roca'
    FENGHUANG = 'Fenghuang'
    ZIZ = 'Ziz'
    SIMURGH = 'Simurgue'
    ITSUMADE = 'Itsumade'
    PHOENIX = 'Fênix'
    QUETZALCOATL = 'Quetzalcóatl'


class MagicalGrimoireMaterialEnum(Enum):
    MERLIN = 'Merlin'
    DUMBLEDORE = 'Dumbledore'
    MEDIVH = 'Medivh'
    ELMINSTER = 'Elminster'
    GANDALF = 'Gandalf'
    SARUMAN = 'Saruman'
    MORGANA = 'Morgana'
    CIRCE = 'Circe'
    HECATE = 'Hecate'


class MagicalStonesMaterialEnum(Enum):
    HEMATITE = 'Hematita'
    AGATE = 'Ágata'
    MALACHITE = 'Malaquita'
    LAPIS_LAZULI = 'Lápis Lazúli'
    JADE = 'Jade'
    AMETHYST = 'Ametista'
    AMBER = 'Âmbar'
    OPAL = 'Opala'
    EMERALD = 'Esmeralda'


class WearableMaterialEnum(Enum):
    LEATHER = 'Couro'
    BONE = 'Osso'
    COPPER = 'Cobre'
    IRON = 'Ferro'
    STEEL = 'Aço'
    OBSIDIAN = 'Obsidiana'
    RUNITE = 'Runita'
    ADAMANTIUM = 'Adamantium'
    MITHRIL = 'Mitril'


class MagicalWearableMaterialEnum(Enum):
    ALBERS = 'Albers'
    BEUTLICH = 'Beutlich'
    COLLINGWOOD = 'Collingwood'
    DARSEN = 'Darsen'
    EISLER = 'Eisler'
    FAWNEY = 'Fawney'
    GARSEN = 'Garsen'
    HOTH = 'Hoth'
    INA = 'Ina'


class MagicalMaskMaterialEnum(Enum):
    BARONG = 'Barong'  # Lembra uma Pantera (Indonésia)
    CALAVERA = 'Calavera'  # Caveira mexicana
    HANNYA = 'Hannya'  # japonês, representando um demônio feminino ciumento
    HUAXIA = 'Huaxia'  # Ópera de Pequim
    KABUKI = 'Kabuki'  # Teatro japonês
    KACHINA = 'Kachina'  # Estilo a máscara do Crash (Povos Nativos Americanos)
    TENGU = 'Tengu'  # Narigão vermelho
    VENETIAN = 'Venetian'  # Carnaval
    ZANNI = 'Zanni'  # Nariguda italiana


class TacticalWearableMaterialEnum(Enum):
    CLOTH = 'Pano'
    LEATHER = 'Couro'
    MINK = 'Vison'
    MOLESKIN = 'Moleskine'
    CHIFFON = 'Chiffon'  # Musseline
    SILK = 'Seda'
    WYVERN_SCALES = 'Escamas de Serpe'
    NEMEAN_LEATHER = 'Couro de Neméia'
    CHAIN_MITHRIL = 'Anéis de Mitril'


class AccessoryMaterialsEnum(Enum):
    BRONZE = 'Bronze'
    SILVER = 'Prata'
    GOLD = 'Ouro'
    PEARL = 'Pérola'
    PLATINUM = 'Platina'
    DIAMOND = 'Diamante'
