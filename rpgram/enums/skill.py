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


class ArcanistSkillEnum(Enum):
    FIRE_RAY = 'Raio de Fogo'
    FIRE_WAVE = 'Onda de Fogo'
    MAGMA_GEYSER = 'Gêiser de Magma'
    SWIRL = 'Redemoinho'
    SAND_GUST = 'Rajada de Areia'
    MUD_TRAP = 'Armadilha de Lama'
    TETRAGRAM_SHOT = 'Disparo Tetragrama'
    DARK_SHOT = 'Disparo das Trevas'
    PRISMATIC_ABRUMATION = 'Abrumação Prismática'
    CONCENTRATED_PRISMATIC_SHOT = 'Disparo Prismático Concentrado'
    CONCENTRATED_BICHROMATIC_ABRUMATION = 'Abrumação Bicromática Concentrada'


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


class BerserkirSkillEnum(Enum):
    INDOMITABLE_ATTACK = 'Ataque Indomável'
    IMPETUOUS_STRIKE = 'Golpe Impetuoso'
    DEVASTATING_RUSH = 'Rajada Devastadora'
    HRUNGNIRÇÇÇS_SOVEREIGNTY = 'Soberania de Hrungnir'
    FENRIRÇÇÇS_INSTINCT = 'Instinto de Fenrir'
    YMIRÇÇÇS_RESILIENCE = 'Resiliência de Ymir'
    STONE_STRIKE = 'Golpe de Pedra'
    FROST_BITE = 'Mordida de Gelo'
    ANCIENT_FURY = 'Fúria Anciã'


class BountyHunterSkillEnum(Enum):
    STAB = 'Apunhalar'
    QUICK_DRAW = 'Saque Rápido'
    SURPRISE_ATTACK = 'Ataque Surpresa'
    HUNTING_NET = 'Rede de Caça'
    CHOMP_TRAP = 'Armadilha Chomp'
    SHARP_FARO = 'Faro Aguçado'
    INVESTIGATION = 'Investigação'
    GLOW_BURST = 'Brilhestouro'
    GLOW_BURST_VOLLEY = 'Saraivada de Brilhestouros'
    GIGA_GLOW_BURST = 'Giga Brilhestouro'


class BardSkillEnum(Enum):
    DISSONANCE = 'Dissonância'
    RESONANCE = 'Resonância'
    FATAL_CHORD = 'Acorde Fatal'
    SUPERSONIC = 'Supersônico'
    WAR_SONG = 'Canção de Guerra'
    CRESCENT_MOON_BALLAD = 'Balada da Lua Crescente'
    TRICKSTER_TROVA = 'Trova do Malandro'
    INVIGORATING_SONG = 'Canto Revigorante'


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


class DuelistSkillEnum(Enum):
    WIND_BLADE = 'Lâmina de Vento'
    SPLASH_FOUNT = "Fontaine D'éclaboussure"
    AGILE_FEET = 'Pés Ágeis'
    EAGLE_EYE = 'Olho de Águia'
    LUNGE = 'Estocada'
    TRANSPASS = 'Transpassar'
    INVERSE = 'Inversa'
    DIRTY_BLOW = 'Golpe Sujo'
    ACHILLEÇÇÇS_HEEL = 'Calcanhar de Aquiles'
    DISARMOR = 'Desarmadurar'
    SIEGFRIEDÇÇÇS_SHOULDER_BLADE = 'Omoplata de Siegfried'


class GladiatorSkillEnum(Enum):
    ACHILLES_ATTACK = 'Ataque de Aquiles'
    HERCULES_FURY = 'Fúria de Hércules'
    ARES_BLADE = 'Lâmina de Ares'
    AJAX_SHIELD = 'Escudo de Ajax'
    TURTLE_STANCE = 'Postura de Tartaruga'
    UNICORN_STANCE = 'Postura de Unicórnio'
    ARENA_DOMAIN = 'Domínio da Arena'
    MARTIAL_BANNER = 'Estandarte Marcial'
    FLAMING_FURY = 'Fúria Flamejante'
    FLAMING_FURY_BLADE = 'Lâmina de Fúria Flamejante'
    WAR_CORNU = 'Cornu de Guerra'


class GuardianSkillEnum(Enum):
    SHIELD_WALL = 'Parede de Escudos'
    IRON_CHARGE = 'Investida de Ferro'
    STEEL_STORM = 'Tempestade de Aço'
    CRYSTAL_ARMOR = 'Armadura de Cristal'
    CRYSTALLINE_INFUSION = 'Infusão Cristalina'
    SHATTER = 'Despedaçar'
    CRYSTAL_CHRYSALIS = 'Crisálida de Cristal'


class HealerSkillEnum(Enum):
    HEALING_TOUCH = 'Toque de Cura'
    HEALING_HERB = 'Erva Curativa'
    VITALITY_AURA = 'Aura de Vitalidade'
    PROTECTIVE_AURA = 'Aura Protetiva'
    REVIVE_RITUAL = 'Ritual de Reviver'
    HEALING_REFUGE = 'Refúgio Curativo'
    PROTECTIVE_INFUSION = 'Infusão Protetiva'
    BEATIFYING_AEGIS = 'Aegís Beatificante'


class HeraldSkillEnum(Enum):
    MYSTIC_BLOCK = 'Bloqueio Místico'
    ROBYSTIC_SHIELD = 'Escudo Robístico'
    ROBYSTIC_BLOCK = 'Bloqueio Robístico'
    COLOSSAL_ONSLAUGHT = 'Investida Colossal'
    VIGIL_FLAME = 'Chama Vigílica'
    FLAME_MANTILLA = 'Mantilha de Chamas'
    IGNEOUS_STRIKE = 'Golpe Ígneo'
    FLAMES_OF_EQUILIBRIUM = 'Chamas do Equilíbrio'
    BLUE_EQUILIBRIUM = 'Equilíbrio Azul'
    RED_EQUILIBRIUM = 'Equilíbrio Vermelho'
    PURIFYING_FLAME = 'Chama Purificadora'
    IGNEOUS_HEART = 'Coração Ígneo'
    PURIFYING_HEART = 'Coração Purificador'

    # Special Damage
    VIGIL_ARMS = 'Braços Vigílicos'
    MANTILLED_ARMS = 'Braços Mantilhados'


class KnightSkillEnum(Enum):
    CHARGE = 'Carga'
    HEAVY_CHARGE = 'Carga Pesada'
    SUPER_CHARGE = 'Super Carga'
    CHAMPION_INSPIRATION = 'Inspiração Campeã'
    LEADERSHIP = 'Liderança'
    ROYAL_FURY = 'Fúria Régia'
    JUSTICE_BLADE = 'Lâmina da Justiça'
    SOVEREIGN_CUT = 'Corte Soberano'
    ROYAL_SHIELD = 'Escudo Real'


class LordOfTheRoguesSkillEnum(Enum):
    SILENT_ASSASSIN = 'Assassino Silencioso'
    DEADLY_BLADE = 'Lâmina Mortal'


class MageSkillEnum(Enum):
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


class MercenarySkillEnum(Enum):
    NOSEBREAKER = 'Quebra-Venta'
    SKULLBREAKER = 'Quebra-Crânio'
    IMPROVISE = 'Improvisar'


class NecromancerSkillEnum(Enum):
    BANNED_SOUL = 'Alma Penada'
    VENGEFUL_SPIRIT = 'Espírito Vingativo'
    UNDEAD_EMBRACE = 'Abraço de Morto-Vivo'
    ABYSSAL_CREATURE = 'Criatura Abissal'
    THE_HORDE = 'A Horda'
    BONE_BUCKLER = 'Broquel de Osso'
    BONE_SPAULDER = 'Espaldeira de Osso'
    BONE_ARMOR = 'Armadura de Osso'


class PaladinSkillEnum(Enum):
    SACRED_BALM = 'Bálsamo Sagrado'
    GREENDRAGON_BALM = 'Bálsamo de Dragão Verde'
    REDPHOENIX_BALM = 'Bálsamo de Fênix Vermelha'
    BLUEDJINN_BALM = 'Bálsamo de Djinn Azul'
    SQUIRE_ANOINTING = 'Unção do Escudeiro'
    WARRIOR_ANOINTING = 'Unção do Guerreiro'
    MAIDEN_ANOINTING = 'Unção da Donzela'
    KNIGHT_ANOINTING = 'Unção do Cavaleiro'
    COURTESAN_ANOINTING = 'Unção da Cortesã'
    LORD_ANOINTING = 'Unção do Lorde'
    EXCALIBUR = 'Excalibur'
    KUSANAGI_NO_TSURUGI = 'Kusanagi-no-Tsurugi'
    TYRFING = 'Tirfing'
    OSHE = 'Oxé'
    SUDARSHANA_CHAKRA = 'Sudarshana Chakra'
    GUNGNIR = 'Gungnir'
    FLOGGINGS = 'Flagelações'
    CUT_THROAT = 'Degolar'
    VLADS_PUNISHMENT = 'Punição de Vlad'
    CONFESSION = 'Confissão'
    PENITENCE = 'Penitência'
    CONFISCATION = 'Confisco'
    EXCOMMUNICATE = 'Excomungar'
    EXILE = 'Exílio'


class RangerSkillEnum(Enum):
    K9_STRIKE = 'Golpe K9'
    DOUBLE_AMBUSH = 'Emboscada Dupla'
    THE_PACK = 'A Matilha'
    SNIFF = 'Farejar'
    ALERT = 'Alerta'


class RogueSkillEnum(Enum):
    VIPERÇÇÇS_FANGS = 'Presas de Víbora'
    DOUBLE_FANGS = 'Presas Duplas'
    TAIPAN_INOCULATE = 'Inocula de Taipan'
    PHANTOM_STRIKE = 'Golpe Fantasma'
    ELUSIVE_ASSAULT = 'Investida Elusiva'
    SHADOW_STEPS = 'Passos Sombrios'
    CHAOTIC_STEPS = 'Passos Caóticos'
    SHADOW_STRIKE = 'Golpe Sombrio'
    CHAOTIC_STRIKE = 'Golpe Caótico'


class SamuraiSkillEnum(Enum):
    KOTE_UCHI = 'Kote-Uchi'
    DO_UCHI = 'Dô-Uchi'
    MEN_UCHI = 'Men-Uchi'
    ZANTETSUSEN = 'Zantetsusen'  # Slashing Steel Flash
    MIZU_KOGEKI = 'Mizu Kōgeki'  # Água
    HONO_KOGEKI = 'Honō Kōgeki'  # Chamas
    KOSEN_KOGEKI = 'Kōsen Kōgeki'  # Raio
    KAZE_KOGEKI = 'Kaze Kōgeki'  # Vento
    IWA_KOGEKI = 'Iwa Kōgeki'  # Rocha


class ShamanSkillEnum(Enum):
    VINE_CROSIER = 'Báculo de Vinha'
    WILD_CARNATION_CLOAK = 'Manto de Cravo Selvagem'
    CRYSTAL_SAP_RING = 'Anel de Seiva Cristalina'
    FIGHTER_PANDINUS = 'Pandinus Lutador'
    FELLOW_PANDINUS = 'Pandinus Companheiro'
    PROTECTOR_TURTLE = 'Tartaruga Protetora'
    FELLOW_TURTLE = 'Tartaruga Companheira'
    CLAIRVOYANT_WOLF = 'Lobo Clarividente'
    FELLOW_WOLF = 'Lobo Companheiro'
    LOOKOUTER_YETI = 'Yeti Olhador'
    FELLOW_YETI = 'Yeti Companheiro'
    ROCK_PANDINUS = 'Pandinus de Rocha'
    MAELSTROM = 'Voragem'
    LASER_CLAW = 'Garra Laser'
    SNOW_BREATH = 'Sopro de Neve'


class SorcererSkillEnum(Enum):
    MYSTICAL_PROTECTION = 'Proteção Mística'
    MYSTICAL_CONFLUENCE = 'Confluência Mística'
    MYSTICAL_VIGOR = 'Vigor Místico'
    PRISMATIC_SCINTILLATION = 'Cintilação Prismática'
    PRISMATIC_SHIELD = 'Escudo Prismático'
    CHAOS_ORB = 'Orbe do Caos'
    CHAOS_VAMPIRISM = 'Vampirismo do Caos'
    CHAOS_WEAVER = 'Tecelão do Caos'


class SorcererSupremeSkillEnum(Enum):
    MAGIC_ORB = 'Orbe Mágico'
    MAGICAL_IMPRISONMENT = 'Aprisionamento Mágico'
    MAGIC_SHIELD = 'Escudo Mágico'
    MAGIC_SHOT = 'Disparo Mágico'


class SummonerSkillEnum(Enum):
    FLAMING_SPECTER = 'Espectro Flamejante'
    KAPPA_FOUNTAIN = 'Fonte do Kappa'
    PISKIE_WINDBAG = 'Sacovento do Piskie'


class WarriorSkillEnum(Enum):
    POWERFUL_ATTACK = 'Ataque Poderoso'
    MORE_THAN_POWERFUL_ATTACK = 'Ataque Mais Que Poderoso'
    MUCH_MORE_THAN_POWERFUL_ATTACK = 'Ataque Muito Mais Que Poderoso'
    BLINK_ATTACK = 'Ataque Lampejante'
    LETHAL_ATTACK = 'Ataque Letal'
    AEGIS_SHADOW = 'Sombra de Égide'
    WAR_BANNER = 'Flâmula de Guerra'
    HEROIC_INSPIRATION = 'Inspiração Heroíca'
    WAR_CRY = 'Grito de Guerra'


class WeaponMasterSkillEnum(Enum):
    SLASHING_ATTACK = 'Ataque Talhante'
    SONIC_BLADE = 'Lâmina Sônica'
    VORPAL_BLADE_ATTACK = 'Ataque da Lâmina Vorpal'
    BRUISING_ATTACK = 'Ataque Contudente'
    CRYSTALLINE_CLASH = 'Choque Cristalino'
    GEOCRUSHER_ATTACK = 'Ataque Geoesmagador'
    TERREBRANT_ATTACK = 'Ataque Terebrante'
    THUNDERPASS = 'Trovanspassar'
    STORM_DANCE = 'Dança da Tempestade'


class MultiClasseSkillEnum(Enum):
    QUICK_ATTACK = 'Ataque Rápido'
    ROBUST_BLOCK = 'Bloqueio Robusto'
    GUARDIAN_SHIELD = 'Escudo Guardião'
    HEAVY_CHARGE = 'Investida Pesada'
    FIRE_BALL = 'Bola de Fogo'
    WATER_BUBBLE = 'Bolha de Água'
    WIND_GUST = 'Rajada de Vento'
    EARTH_BREAK = 'Quebra-Terra'
    PRISMATIC_SHOT = 'Disparo Prismático'


TARGET_ENUM_NOT_SELF = [TargetEnum.SINGLE, TargetEnum.TEAM, TargetEnum.ALL]
MAGICAL_DEFENSE_ENUM_LIST = [SkillDefenseEnum.MAGICAL]
PHYSICAL_DEFENSE_ENUM_LIST = [SkillDefenseEnum.PHYSICAL, SkillDefenseEnum.TRUE]
