from enum import Enum


class WeaponMaterialEnum(Enum):
    WOOD = 'madeira'
    BONE = 'osso'
    COPPER = 'cobre'
    IRON = 'ferro'
    STEEL = 'aço'
    OBSIDIAN = 'obsidiana'
    RUNITE = 'runita'
    MITHRIL = 'mitril'
    ADAMANTIUM = 'adamantium'


class QuillMaterialEnum(Enum):
    YATAGARASU = 'corvo-de-três-pernas'
    HARPIA = 'harpia'
    ROC = 'roca'
    FENGHUANG = 'fenghuang'
    ZIZ = 'ziz'
    SIMURGH = 'simurgue'
    ITSUMADE = 'itsumade'
    PHOENIX = 'fênix'
    QUETZALCOATL = 'quetzalcóatl'


class GrimoireMaterialEnum(Enum):
    MERLIN = 'merlin'
    DUMBLEDORE = 'dumbledore'
    MEDIVH = 'medivh'
    ELMINSTER = 'elminster'
    GANDALF = 'gandalf'
    SARUMAN = 'saruman'
    MORGANA = 'morgana'
    CIRCE = 'circe'
    HECATE = 'hecate'


class MagicalStonesMaterialEnum(Enum):
    HEMATITE = 'hematita'
    AGATE = 'ágata'
    MALACHITE = 'malaquita'
    LAPIS_LAZULI = 'lápis lazúli'
    JADE = 'jade'
    AMETHYST = 'ametista'
    AMBER = 'âmbar'
    OPAL = 'opala'
    EMERALD = 'esmeralda'


class WearableMaterialEnum(Enum):
    CLOTH = 'pano'
    LEATHER = 'couro'
    BONE = 'osso'
    COPPER = 'cobre'
    IRON = 'ferro'
    STEEL = 'aço'
    RUNITE = 'runita'
    MITHRIL = 'mitril'
    ADAMANTIUM = 'adamantium'


class MagicalWearableMaterialEnum(Enum):
    ALBERS = 'albers'
    BEUTLICH = 'beutlich'
    COLLINGWOOD = 'collingwood'
    DARSEN = 'darsen'
    EISLER = 'eisler'
    FAWNEY = 'fawney'
    GARSEN = 'garsen'
    HOTH = 'hoth'
    INA = 'ina'


class MaskMaterialEnum(Enum):
    BARONG = 'barong'  # Lembra uma Pantera (Indonésia)
    CALAVERA = 'calavera'  # Caveira mexicana
    HANNYA = 'hannya'  # japonês, representando um demônio feminino ciumento
    HUAXIA = 'huaxia'  # Ópera de Pequim
    KABUKI = 'kabuki'  # Teatro japonês
    KACHINA = 'kachina'  # Estilo a máscara do Crash (Povos Nativos Americanos)
    TENGU = 'tengu'  # Narigão vermelho
    VENETIAN = 'venetian'  # Carnaval
    ZANNI = 'zanni'  # Nariguda italiana


class AccessoryMaterialsEnum(Enum):
    BRONZE = 'bronze'
    SILVER = 'prata'
    GOLD = 'ouro'
    PEARL = 'pérola'
    PLATINUM = 'platina'
    DIAMOND = 'diamante'
