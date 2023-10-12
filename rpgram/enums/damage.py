from enum import Enum


class DamageEnum(Enum):
    HITTING = BLUDGEONING = 'Contusão'
    SLASHING = 'Corte'
    PIERCING = 'Perfuração'
    MAGIC = 'Mágico'
    BLESSING = 'Sagrado'
    DIVINE = 'Divino'
    LIGHT = 'Luz'
    DARK = 'Trevas'
    FIRE = 'Fogo'
    WATER = 'Água'
    COLD = 'Gelo'
    LIGHTNING = 'Raio'
    WIND = 'Vento'
    ROCK = 'Rocha'
    GROUND = 'Terra'
    ACID = 'Ácido'
    POISON = 'Veneno'
    CHAOS = 'Caos'


MAGICAL_DAMAGE_TYPES = (
    DamageEnum.MAGIC,
    DamageEnum.BLESSING,
    DamageEnum.DIVINE,
    DamageEnum.LIGHT,
    DamageEnum.DARK,
    DamageEnum.FIRE,
    DamageEnum.WATER,
    DamageEnum.COLD,
    DamageEnum.LIGHTNING,
    DamageEnum.WIND,
    DamageEnum.ACID,
    DamageEnum.POISON,
    DamageEnum.CHAOS,
)
PHYSICAL_DAMAGE_TYPES = (
    DamageEnum.BLUDGEONING,
    DamageEnum.HITTING,
    DamageEnum.SLASHING,
    DamageEnum.PIERCING,
    DamageEnum.ROCK,
    DamageEnum.GROUND,
)

if __name__ == '__main__':
    damage_enum_length = len(DamageEnum) + 1
    magical_length = len(MAGICAL_DAMAGE_TYPES)
    physical_length = len(PHYSICAL_DAMAGE_TYPES)
    if damage_enum_length == magical_length + physical_length:
        print('DamageEnum OK!!!')
    else:
        raise ValueError(
            'DamageEnum is not OK!!!\n'
            f'damage_enum_length: {damage_enum_length}\n'
            f'magical_length: {magical_length}\n'
            f'physical_length: {physical_length}\n'
        )
