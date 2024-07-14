from enum import Enum
from typing import Union


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
    ROAR = 'Rugido'
    CRYSTAL = 'Cristal'
    BLAST = 'Explosão'


class DamageEmojiEnum(Enum):
    HITTING = BLUDGEONING = '👊'
    SLASHING = '🔪'
    PIERCING = '🏹'
    MAGIC = '🪄'
    BLESSING = '😇'
    DIVINE = '🪬'
    LIGHT = '🔆'
    DARK = '🌑'
    FIRE = '🔥'
    WATER = '🌊'
    COLD = '❄️'
    LIGHTNING = '⚡️'
    WIND = '🌪'  # 💨
    ROCK = '🪨'
    GROUND = '🟤'
    ACID = '🍋'
    POISON = '🐍'
    CHAOS = '🦇'
    ROAR = '🦁'
    CRYSTAL = '🟣'
    BLAST = '🧨'


def get_damage_emoji_text(damage: Union[DamageEnum, str]) -> str:
    if isinstance(damage, str):
        damage = DamageEnum[damage]
    name = damage.name
    return f'{DamageEmojiEnum[name].value}{damage.value}'


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
    DamageEnum.CRYSTAL,
)
PHYSICAL_DAMAGE_TYPES = (
    DamageEnum.BLUDGEONING,
    DamageEnum.HITTING,
    DamageEnum.SLASHING,
    DamageEnum.PIERCING,
    DamageEnum.ROCK,
    DamageEnum.GROUND,
    DamageEnum.ROAR,
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
