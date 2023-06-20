from enum import Enum


class DamageEnum(Enum):
    HITTING = BLUDGEONING = 'contusão'
    SLASHING = 'corte'
    PIERCING = 'perfuração'
    MAGIC = 'mágico'
    BLESSING = DIVINE = 'sagrado'
    LIGHT = 'luz'
    DARK = 'trevas'
    FIRE = 'fogo'
    WATER = 'água'
    COLD = 'gelo'
    LIGHTNING = 'raio'
    ROCK = GROUND = 'rocha'
    ACID = 'ácido'
    POISON = 'veneno'
    CHAOS = 'caos'
