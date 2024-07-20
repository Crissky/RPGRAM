from typing import TYPE_CHECKING, List, Type, Union

from rpgram.enums.classe import ClasseEnum
from rpgram.skills.classes.barbarian.factory import (
    BARBARIAN_SKILL_LIST,
    barbarian_skill_factory
)
from rpgram.skills.classes.cleric.factory import (
    CLERIC_SKILL_LIST,
    cleric_skill_factory
)
from rpgram.skills.classes.guardian.factory import (
    guardian_skill_factory,
    GUARDIAN_SKILL_LIST
)
from rpgram.skills.classes.mage.factory import (
    MAGE_SKILL_LIST,
    mage_skill_factory
)
from rpgram.skills.classes.sorcerer.factory import (
    SORCERER_SKILL_LIST,
    sorcerer_skill_factory
)
from rpgram.skills.classes.warrior.factory import (
    WARRIOR_SKILL_LIST,
    warrior_skill_factory
)
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


ALL_SKILL_DICT = {
    'Bárbaro': BARBARIAN_SKILL_LIST,
    'Clérigo': CLERIC_SKILL_LIST,
    'Feiticeiro': SORCERER_SKILL_LIST,
    'Guardião': GUARDIAN_SKILL_LIST,
    'Guerreiro': WARRIOR_SKILL_LIST,
    'Mago': MAGE_SKILL_LIST,
}


def skill_factory(
    classe_name: Union[ClasseEnum, str],
    skill_class_name: str,
    char: 'BaseCharacter',
    level: int = 1
) -> BaseSkill:
    '''Retorna uma função factory relacionada ao classe_name
    '''

    if isinstance(classe_name, ClasseEnum):
        classe_name = classe_name.value

    if ClasseEnum.BARBARIAN.value == classe_name:
        class_skill_factory = barbarian_skill_factory
    elif ClasseEnum.CLERIC.value == classe_name:
        class_skill_factory = cleric_skill_factory
    elif ClasseEnum.DRUID.value == classe_name:
        raise ValueError(f'skills factory pra {classe_name} não implementada!')
    elif ClasseEnum.SORCERER.value == classe_name:
        class_skill_factory = sorcerer_skill_factory
    elif ClasseEnum.WARRIOR.value == classe_name:
        class_skill_factory = warrior_skill_factory
    elif ClasseEnum.ROGUE.value == classe_name:
        raise ValueError(f'skills factory pra {classe_name} não implementada!')
    elif ClasseEnum.MAGE.value == classe_name:
        class_skill_factory = mage_skill_factory
    elif ClasseEnum.PALADIN.value == classe_name:
        raise ValueError(f'skills factory pra {classe_name} não implementada!')
    elif ClasseEnum.GUARDIAN.value == classe_name:
        class_skill_factory = guardian_skill_factory
    elif ClasseEnum.DUELIST.value == classe_name:
        raise ValueError(f'skills factory pra {classe_name} não implementada!')
    elif ClasseEnum.HERALD.value == classe_name:
        raise ValueError(f'skills factory pra {classe_name} não implementada!')
    elif ClasseEnum.ARCANIST.value == classe_name:
        raise ValueError(f'skills factory pra {classe_name} não implementada!')
    elif ClasseEnum.BARD.value == classe_name:
        raise ValueError(f'skills factory pra {classe_name} não implementada!')
    elif ClasseEnum.BOUNTY_HUNTER.value == classe_name:
        raise ValueError(f'skills factory pra {classe_name} não implementada!')
    elif ClasseEnum.KNIGHT.value == classe_name:
        raise ValueError(f'skills factory pra {classe_name} não implementada!')
    elif ClasseEnum.HEALER.value == classe_name:
        raise ValueError(f'skills factory pra {classe_name} não implementada!')
    elif ClasseEnum.GLADIATOR.value == classe_name:
        raise ValueError(f'skills factory pra {classe_name} não implementada!')
    elif ClasseEnum.SUMMONER.value == classe_name:
        raise ValueError(f'skills factory pra {classe_name} não implementada!')
    elif ClasseEnum.MERCENARY.value == classe_name:
        raise ValueError(f'skills factory pra {classe_name} não implementada!')
    elif ClasseEnum.NECROMANCER.value == classe_name:
        raise ValueError(f'skills factory pra {classe_name} não implementada!')
    elif ClasseEnum.RANGER.value == classe_name:
        raise ValueError(f'skills factory pra {classe_name} não implementada!')
    elif ClasseEnum.SHAMAN.value == classe_name:
        raise ValueError(f'skills factory pra {classe_name} não implementada!')
    elif ClasseEnum.SAMURAI.value == classe_name:
        raise ValueError(f'skills factory pra {classe_name} não implementada!')
    elif ClasseEnum.BERSERKIR.value == classe_name:
        raise ValueError(f'skills factory pra {classe_name} não implementada!')
    elif ClasseEnum.WEAPON_MASTER.value == classe_name:
        raise ValueError(f'skills factory pra {classe_name} não implementada!')
    elif ClasseEnum.SORCERER_SUPREME.value == classe_name:
        raise ValueError(f'skills factory pra {classe_name} não implementada!')
    elif ClasseEnum.LORD_OF_THE_ROGUES.value == classe_name:
        raise ValueError(f'skills factory pra {classe_name} não implementada!')
    else:
        raise ValueError(f'Classe {classe_name} não encontrada!')

    return class_skill_factory(
        skill_class_name=skill_class_name,
        char=char,
        level=level,
    )


def skill_list_factory(
    classe_name: Union[ClasseEnum, str]
) -> List[Type[BaseSkill]]:
    '''Retorna uma função factory relacionada ao classe_name
    '''

    if isinstance(classe_name, ClasseEnum):
        classe_name = classe_name.value

    if ClasseEnum.BARBARIAN.value == classe_name:
        return BARBARIAN_SKILL_LIST
    elif ClasseEnum.CLERIC.value == classe_name:
        return CLERIC_SKILL_LIST
    elif ClasseEnum.DRUID.value == classe_name:
        raise ValueError(f'skills para {classe_name} ainda não implementada!')
    elif ClasseEnum.SORCERER.value == classe_name:
        return SORCERER_SKILL_LIST
    elif ClasseEnum.WARRIOR.value == classe_name:
        return WARRIOR_SKILL_LIST
    elif ClasseEnum.ROGUE.value == classe_name:
        raise ValueError(f'skills para {classe_name} ainda não implementada!')
    elif ClasseEnum.MAGE.value == classe_name:
        return MAGE_SKILL_LIST
    elif ClasseEnum.PALADIN.value == classe_name:
        raise ValueError(f'skills para {classe_name} ainda não implementada!')
    elif ClasseEnum.GUARDIAN.value == classe_name:
        return GUARDIAN_SKILL_LIST
    elif ClasseEnum.DUELIST.value == classe_name:
        raise ValueError(f'skills para {classe_name} ainda não implementada!')
    elif ClasseEnum.HERALD.value == classe_name:
        raise ValueError(f'skills para {classe_name} ainda não implementada!')
    elif ClasseEnum.ARCANIST.value == classe_name:
        raise ValueError(f'skills para {classe_name} ainda não implementada!')
    elif ClasseEnum.BARD.value == classe_name:
        raise ValueError(f'skills para {classe_name} ainda não implementada!')
    elif ClasseEnum.BOUNTY_HUNTER.value == classe_name:
        raise ValueError(f'skills para {classe_name} ainda não implementada!')
    elif ClasseEnum.KNIGHT.value == classe_name:
        raise ValueError(f'skills para {classe_name} ainda não implementada!')
    elif ClasseEnum.HEALER.value == classe_name:
        raise ValueError(f'skills para {classe_name} ainda não implementada!')
    elif ClasseEnum.GLADIATOR.value == classe_name:
        raise ValueError(f'skills para {classe_name} ainda não implementada!')
    elif ClasseEnum.SUMMONER.value == classe_name:
        raise ValueError(f'skills para {classe_name} ainda não implementada!')
    elif ClasseEnum.MERCENARY.value == classe_name:
        raise ValueError(f'skills para {classe_name} ainda não implementada!')
    elif ClasseEnum.NECROMANCER.value == classe_name:
        raise ValueError(f'skills para {classe_name} ainda não implementada!')
    elif ClasseEnum.RANGER.value == classe_name:
        raise ValueError(f'skills para {classe_name} ainda não implementada!')
    elif ClasseEnum.SHAMAN.value == classe_name:
        raise ValueError(f'skills para {classe_name} ainda não implementada!')
    elif ClasseEnum.SAMURAI.value == classe_name:
        raise ValueError(f'skills para {classe_name} ainda não implementada!')
    elif ClasseEnum.BERSERKIR.value == classe_name:
        raise ValueError(f'skills para {classe_name} ainda não implementada!')
    elif ClasseEnum.WEAPON_MASTER.value == classe_name:
        raise ValueError(f'skills para {classe_name} ainda não implementada!')
    elif ClasseEnum.SORCERER_SUPREME.value == classe_name:
        raise ValueError(f'skills para {classe_name} ainda não implementada!')
    elif ClasseEnum.LORD_OF_THE_ROGUES.value == classe_name:
        raise ValueError(f'skills para {classe_name} ainda não implementada!')
    else:
        raise ValueError(f'Classe {classe_name} não encontrada!')
