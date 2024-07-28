from enum import Enum

from rpgram.enums.emojis import EmojiEnum


class TargetEnum(Enum):
    SELF = 'self'
    SINGLE = 'single'
    TEAM = 'team'
    ALL = 'all'


class SkillTypeEnum(Enum):
    ATTACK = 'attack'
    BARRIER = 'barrier'
    BUFF = 'buff'
    DEFENSE = 'defense'
    HEALING = 'healing'


class SkillDefenseEnum(Enum):
    PHYSICAL = 'physical'
    MAGICAL = 'magical'
    TRUE = 'true'
    NA = 'n/a'


class TargetEmojiEnum(Enum):
    SELF = '🙋'
    SINGLE = '👤'
    TEAM = '👥'
    ALL = '🌐'


class SkillTypeEmojiEnum(Enum):
    ATTACK = EmojiEnum.ATTACK.value
    DEFENSE = EmojiEnum.DEFEND.value
    HEALING = EmojiEnum.HEALING.value
    BUFF = '🎖️'
    BARRIER = EmojiEnum.BARRIER_POINT.value


class SkillDefenseEmojiEnum(Enum):
    PHYSICAL = EmojiEnum.PHYSICAL_ATTACK.value
    MAGICAL = EmojiEnum.MAGICAL_ATTACK.value
    TRUE = '💯'
    NA = '⚫'


class BarbarianSkillEnum(Enum):
    PRIMAL_ATTACK = 'Ataque Primal'
    PRIMAL_STRIKE = 'Golpe Primal'
    PRIMAL_RAM = 'Ariete Primal'
    SEISMIC_IMPACT = 'Impacto Sísmico'
    FURIOUS_FURY = 'Fúria Furiosa'
    FURIOUS_INSTINCT = 'Instinto Furioso'
    FRENZY = 'Frenesi'
    FURIOUS_ROAR = 'Rugido Furioso'
    WILD_FORGE = 'Forja Selvagem'
    SALAMANDERÇÇÇS_BREATH = 'Bafo de Salamandra'
    SWEEPING_ROC = 'Rasante de Roc'
    HYDRAÇÇÇS_FANGS = 'Presas da Hidra'
    RAIJŪÇÇÇS_FOOTSTEPS = 'Passos de Raijū'
    FAFNIRÇÇÇS_SCALES = 'Escamas de Fáfnir'

    # Special Damage
    WILD_FIRE = 'Fogo Selvagem'
    WILD_LIGHTNING = 'Raio Selvagem'
    WILD_WIND = 'Vento Selvagem'
    WILD_ROCK = 'Rocha Selvagem'
    WILD_GROUND = 'Terra Selvagem'
    WILD_ACID = 'Ácido Selvagem'
    WILD_POISON = 'Veneno Selvagem'


class ClericSkillEnum(Enum):
    IDUNNÇÇÇS_APPLE = 'Maçã de Idunn'
    KRATOSÇÇÇS_WRATH = 'Ira de Kratos'
    ULLRÇÇÇS_FOCUS = 'Foco de Ullr'
    HECATEÇÇÇS_FLAMES = 'Chamas de Hecate'
    OGUNÇÇÇS_CLOAK = 'Manto de Ogun'
    ISISÇÇÇS_VEIL = 'Véu de Isis'
    ANANSIÇÇÇS_TRICKERY = 'Artimanha de Anansi'
    VIDARÇÇÇS_BRAVERY = 'Bravura de Vidar'
    ARTEMISÇÇÇS_ARROW = 'Flecha de Artemis'
    CERIDWENÇÇÇS_MAGIC_POTION = 'Poção Mágica de Ceridwen'
    GRACE_OF_THE_PANTHEON = 'Graça do Panteão'
    IXCHELÇÇÇS_AMPHORA = 'Ânfora de Ixchel'
    DHANVANTARIÇÇÇS_AMRITA = 'Amrita de Dhanvantari'
    CONCEALMENT = 'Esconjuro'
    HOLY_FIRE = 'Fogo Sagrado'
    DIVINE_PUNISHMENT = 'Punição Divina'
    WILL_O_THE_WISP = 'Fogo-Fátuo'
    GREEK_FIRE = 'Fogo Grego'


class DruidSkillEnum(Enum):
    RANGER_FALCON = 'Falcão Patrulheiro'
    FELLOW_FALCON = 'Falcão Companheiro'
    GUARDIAN_BEAR = 'Urso Guardião'
    FELLOW_BEAR = 'Urso Companheiro'
    HUNTER_TIGER = 'Tigre Caçador'
    FELLOW_TIGER = 'Tigre Companheiro'
    WATCHER_OWL = 'Coruja Sentinela'
    FELLOW_OWL = 'Coruja Companheira'
    FIRE_BIRD = 'Pássaro de Fogo'
    URSEISMIC_TREMOR = 'Tremor Ursísmico'
    THUNDERING_ONSLAUGHT = 'Ataque Trovejante'
    MAGIC_GALE = 'Vendaval Mágico'
    VINE_WHIP = 'Chicote de Vinha'
    SILK_FLOSS_SWORD = 'Espada de Paineira'
    OAK_WARHAMMER = 'Martelo de Guerra de Carvalho'
    VINE_BUCKLER = 'Broquel de Vinha'
    SILK_FLOSS_SPAULDER = 'Espaldeira de Paineira'
    THORNY_SPAULDER = 'Espaldeira Espinheta'
    OAK_ARMOR = 'Armadura de Carvalho'
    POISONOUS_SAP = 'Seiva Venenosa'
    IGNEOUS_SAP = 'Seiva Ígnea'
    ESCARCHA_SAP = 'Seiva Escarcha'
    SAPIOUS_CUBE = 'Cubo Seivoso'


class GuardianSkillEnum(Enum):
    ROBUST_BLOCK = 'Bloqueio Robusto'
    GUARDIAN_SHIELD = 'Escudo Guardião'
    SHIELD_WALL = 'Parede de Escudos'
    HEAVY_CHARGE = 'Investida Pesada'
    IRON_CHARGE = 'Investida de Ferro'
    STEEL_STORM = 'Tempestade de Aço'
    CRYSTAL_ARMOR = 'Armadura de Cristal'
    CRYSTALLINE_INFUSION = 'Infusão Cristalina'
    SHATTER = 'Despedaçar'
    CRYSTAL_CHRYSALIS = 'Crisálida de Cristal'


class MageSkillEnum(Enum):
    FIRE_BALL = 'Bola de Fogo'
    WATER_BUBBLE = 'Bolha de Água'
    WIND_GUST = 'Rajada de Vento'
    EARTH_BREAK = 'Quebra-Terra'
    MAGIC_BLAST = 'Explosão Mágica'
    ICE_SHARD = 'Fragmento de Gelo'
    ROCK_ARMOR = 'Armadura de Rocha'
    FULMINANT_LIGHTNING = 'Raio Fulminante'
    SCORCHING_BREATH = 'Sopro Escaldante'
    FIRE_STORM = 'Tormenta de Fogo'
    LAVA_SKIN = 'Pele de Lava'
    MIST_FORM = 'Forma de Névoa'
    MUD_SHOT = 'Disparo de Lama'
    MUDDY = 'Enlameado'
    SAND_STORM = 'Tempestade de Areia'


class MultiClasseSkillEnum(Enum):
    QUICK_ATTACK = 'Ataque Rápido'


class RogueSkillEnum(Enum):
    VIPERÇÇÇS_FANGS = 'Presas de Víbora'
    DOUBLE_FANGS = 'Presas Duplas'
    TAIPAN_INOCULATE = 'Inocula de Taipan'
    PHANTOM_STRIKE = 'Golpe Fantasma'
    ELUSIVE_ASSAULT = 'Investida Elusiva'
    SHADOW_STEPS = 'Passos Sombrios'
    CHAOTIC_STEPS = 'Passos Caóticos'


class SorcererSkillEnum(Enum):
    MYSTICAL_PROTECTION = 'Proteção Mística'
    MYSTICAL_CONFLUENCE = 'Confluência Mística'
    MYSTICAL_VIGOR = 'Vigor Místico'
    PRISMATIC_SHOT = 'Disparo Prismático'
    PRISMATIC_SCINTILLATION = 'Cintilação Prismática'
    PRISMATIC_SHIELD = 'Escudo Prismático'
    CHAOS_ORB = 'Orbe do Caos'
    CHAOS_VAMPIRISM = 'Vampirismo do Caos'
    CHAOS_WEAVER = 'Tecelão do Caos'


class WarriorSkillEnum(Enum):
    POWERFUL_ATTACK = 'Ataque Poderoso'
    MORE_THAN_POWERFUL_ATTACK = 'Ataque Mais Que Poderoso'
    BLINK_ATTACK = 'Ataque Lampejante'
    LETHAL_ATTACK = 'Ataque Letal'
    AEGIS_SHADOW = 'Sombra de Égide'
    WAR_BANNER = 'Flâmula de Guerra'
    HEROIC_INSPIRATION = 'Inspiração Heroíca'
    WAR_CRY = 'Grito de Guerra'


TARGET_ENUM_NOT_SELF = [TargetEnum.SINGLE, TargetEnum.TEAM, TargetEnum.ALL]
MAGICAL_DEFENSE_ENUM_LIST = [SkillDefenseEnum.MAGICAL]
PHYSICAL_DEFENSE_ENUM_LIST = [SkillDefenseEnum.PHYSICAL, SkillDefenseEnum.TRUE]
