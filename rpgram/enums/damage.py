from enum import Enum


class DamageEnum(Enum):
    hitting = bludgeoning = 'Contusão'
    slashing = 'Corte'
    piercing = 'Perfuração'
    magic = 'Mágico'
    blessing = divine = 'Sagrado'
    light = 'Luz'
    dark = 'Trevas'
    fire = 'Fogo'
    water = 'Água'
    cold = 'Gelo'
    lightning = 'Raio'
    rock = ground = 'Rocha'
    acid = 'Ácido'
    poison = 'Veneno'
    chaos = 'Caos'