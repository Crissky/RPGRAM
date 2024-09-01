from typing import TYPE_CHECKING, List, Type, Union

from rpgram.enums.classe import ClasseEnum
from rpgram.skills.classes.arcanist.factory import (
    ARCANIST_SKILL_LIST,
    ARCANIST_SKILL_WAYS,
    arcanist_skill_factory
)
from rpgram.skills.classes.barbarian.factory import (
    BARBARIAN_SKILL_LIST,
    BARBARIAN_SKILL_WAYS,
    barbarian_skill_factory
)
from rpgram.skills.classes.bard.factory import (
    BARD_SKILL_LIST,
    BARD_SKILL_WAYS,
    bard_skill_factory
)
from rpgram.skills.classes.berserkir.factory import (
    BERSERKIR_SKILL_LIST,
    BERSERKIR_SKILL_WAYS,
    berserkir_skill_factory
)
from rpgram.skills.classes.bounty_hunter.factory import (
    BOUNTY_HUNTER_SKILL_LIST,
    BOUNTY_HUNTER_SKILL_WAYS,
    bounty_hunter_skill_factory
)
from rpgram.skills.classes.cleric.factory import (
    CLERIC_SKILL_LIST,
    CLERIC_SKILL_WAYS,
    cleric_skill_factory
)
from rpgram.skills.classes.druid.factory import (
    DRUID_SKILL_LIST,
    DRUID_SKILL_WAYS,
    druid_skill_factory
)
from rpgram.skills.classes.duelist.factory import (
    DUELIST_SKILL_LIST,
    DUELIST_SKILL_WAYS,
    duelist_skill_factory
)
from rpgram.skills.classes.gladiator.factory import (
    GLADIATOR_SKILL_LIST,
    GLADIATOR_SKILL_WAYS,
    gladiator_skill_factory
)
from rpgram.skills.classes.guardian.factory import (
    GUARDIAN_SKILL_WAYS,
    guardian_skill_factory,
    GUARDIAN_SKILL_LIST
)
from rpgram.skills.classes.healer.factory import (
    HEALER_SKILL_LIST,
    HEALER_SKILL_WAYS,
    healer_skill_factory
)
from rpgram.skills.classes.herald.factory import (
    HERALD_SKILL_LIST,
    HERALD_SKILL_WAYS,
    herald_skill_factory
)
from rpgram.skills.classes.knight.factory import (
    KNIGHT_SKILL_LIST,
    KNIGHT_SKILL_WAYS,
    knight_skill_factory
)
from rpgram.skills.classes.mage.factory import (
    MAGE_SKILL_LIST,
    MAGE_SKILL_WAYS,
    mage_skill_factory
)
from rpgram.skills.classes.mercenary.factory import (
    MERCENARY_SKILL_LIST,
    MERCENARY_SKILL_WAYS,
    mercenary_skill_factory
)
from rpgram.skills.classes.necromancer.factory import (
    NECROMANCER_SKILL_LIST,
    NECROMANCER_SKILL_WAYS,
    necromancer_skill_factory
)
from rpgram.skills.classes.paladin.factory import (
    PALADIN_SKILL_LIST,
    PALADIN_SKILL_WAYS,
    paladin_skill_factory
)
from rpgram.skills.classes.ranger.factory import (
    RANGER_SKILL_LIST,
    RANGER_SKILL_WAYS,
    ranger_skill_factory
)
from rpgram.skills.classes.rogue.factory import (
    ROGUE_SKILL_LIST,
    ROGUE_SKILL_WAYS,
    rogue_skill_factory
)
from rpgram.skills.classes.shaman.factory import (
    SHAMAN_SKILL_LIST,
    SHAMAN_SKILL_WAYS,
    shaman_skill_factory
)
from rpgram.skills.classes.sorcerer.factory import (
    SORCERER_SKILL_LIST,
    SORCERER_SKILL_WAYS,
    sorcerer_skill_factory
)
from rpgram.skills.classes.summoner.factory import (
    SUMMONER_SKILL_LIST,
    SUMMONER_SKILL_WAYS,
    summoner_skill_factory
)
from rpgram.skills.classes.warrior.factory import (
    WARRIOR_SKILL_LIST,
    WARRIOR_SKILL_WAYS,
    warrior_skill_factory
)
from rpgram.skills.classes.weapon_master.factory import (
    WEAPON_MASTER_SKILL_LIST,
    WEAPON_MASTER_SKILL_WAYS,
    weapon_master_skill_factory
    )
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


ALL_SKILL_DICT = {
    ClasseEnum.BARBARIAN.value: BARBARIAN_SKILL_LIST,
    ClasseEnum.CLERIC.value: CLERIC_SKILL_LIST,
    ClasseEnum.DRUID.value: DRUID_SKILL_LIST,
    ClasseEnum.SORCERER.value: SORCERER_SKILL_LIST,
    ClasseEnum.WARRIOR.value: WARRIOR_SKILL_LIST,
    ClasseEnum.ROGUE.value: ROGUE_SKILL_LIST,
    ClasseEnum.MAGE.value: MAGE_SKILL_LIST,
    ClasseEnum.PALADIN.value: PALADIN_SKILL_LIST,
    ClasseEnum.GUARDIAN.value: GUARDIAN_SKILL_LIST,
    ClasseEnum.DUELIST.value: DUELIST_SKILL_LIST,
    ClasseEnum.HERALD.value: HERALD_SKILL_LIST,
    ClasseEnum.ARCANIST.value: ARCANIST_SKILL_LIST,
    ClasseEnum.BARD.value: BARD_SKILL_LIST,
    ClasseEnum.BOUNTY_HUNTER.value: BOUNTY_HUNTER_SKILL_LIST,
    ClasseEnum.KNIGHT.value: KNIGHT_SKILL_LIST,
    ClasseEnum.HEALER.value: HEALER_SKILL_LIST,
    ClasseEnum.GLADIATOR.value: GLADIATOR_SKILL_LIST,
    ClasseEnum.SUMMONER.value: SUMMONER_SKILL_LIST,
    ClasseEnum.MERCENARY.value: MERCENARY_SKILL_LIST,
    ClasseEnum.NECROMANCER.value: NECROMANCER_SKILL_LIST,
    ClasseEnum.RANGER.value: RANGER_SKILL_LIST,
    ClasseEnum.SHAMAN.value: SHAMAN_SKILL_LIST,
    ClasseEnum.BERSERKIR.value: BERSERKIR_SKILL_LIST,
    ClasseEnum.WEAPON_MASTER.value: WEAPON_MASTER_SKILL_LIST,
}
ALL_SKILL_WAY_DICT = {
    ClasseEnum.BARBARIAN.value: BARBARIAN_SKILL_WAYS,
    ClasseEnum.CLERIC.value: CLERIC_SKILL_WAYS,
    ClasseEnum.DRUID.value: DRUID_SKILL_WAYS,
    ClasseEnum.SORCERER.value: SORCERER_SKILL_WAYS,
    ClasseEnum.WARRIOR.value: WARRIOR_SKILL_WAYS,
    ClasseEnum.ROGUE.value: ROGUE_SKILL_WAYS,
    ClasseEnum.MAGE.value: MAGE_SKILL_WAYS,
    ClasseEnum.PALADIN.value: PALADIN_SKILL_WAYS,
    ClasseEnum.GUARDIAN.value: GUARDIAN_SKILL_WAYS,
    ClasseEnum.DUELIST.value: DUELIST_SKILL_WAYS,
    ClasseEnum.HERALD.value: HERALD_SKILL_WAYS,
    ClasseEnum.ARCANIST.value: ARCANIST_SKILL_WAYS,
    ClasseEnum.BARD.value: BARD_SKILL_WAYS,
    ClasseEnum.BOUNTY_HUNTER.value: BOUNTY_HUNTER_SKILL_WAYS,
    ClasseEnum.KNIGHT.value: KNIGHT_SKILL_WAYS,
    ClasseEnum.HEALER.value: HEALER_SKILL_WAYS,
    ClasseEnum.GLADIATOR.value: GLADIATOR_SKILL_WAYS,
    ClasseEnum.SUMMONER.value: SUMMONER_SKILL_WAYS,
    ClasseEnum.MERCENARY.value: MERCENARY_SKILL_WAYS,
    ClasseEnum.NECROMANCER.value: NECROMANCER_SKILL_WAYS,
    ClasseEnum.RANGER.value: RANGER_SKILL_WAYS,
    ClasseEnum.SHAMAN.value: SHAMAN_SKILL_WAYS,
    ClasseEnum.BERSERKIR.value: BERSERKIR_SKILL_WAYS,
    ClasseEnum.WEAPON_MASTER.value: WEAPON_MASTER_SKILL_WAYS,
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
        class_skill_factory = druid_skill_factory
    elif ClasseEnum.SORCERER.value == classe_name:
        class_skill_factory = sorcerer_skill_factory
    elif ClasseEnum.WARRIOR.value == classe_name:
        class_skill_factory = warrior_skill_factory
    elif ClasseEnum.ROGUE.value == classe_name:
        class_skill_factory = rogue_skill_factory
    elif ClasseEnum.MAGE.value == classe_name:
        class_skill_factory = mage_skill_factory
    elif ClasseEnum.PALADIN.value == classe_name:
        class_skill_factory = paladin_skill_factory
    elif ClasseEnum.GUARDIAN.value == classe_name:
        class_skill_factory = guardian_skill_factory
    elif ClasseEnum.DUELIST.value == classe_name:
        class_skill_factory = duelist_skill_factory
    elif ClasseEnum.HERALD.value == classe_name:
        class_skill_factory = herald_skill_factory
    elif ClasseEnum.ARCANIST.value == classe_name:
        class_skill_factory = arcanist_skill_factory
    elif ClasseEnum.BARD.value == classe_name:
        class_skill_factory = bard_skill_factory
    elif ClasseEnum.BOUNTY_HUNTER.value == classe_name:
        class_skill_factory = bounty_hunter_skill_factory
    elif ClasseEnum.KNIGHT.value == classe_name:
        class_skill_factory = knight_skill_factory
    elif ClasseEnum.HEALER.value == classe_name:
        class_skill_factory = healer_skill_factory
    elif ClasseEnum.GLADIATOR.value == classe_name:
        class_skill_factory = gladiator_skill_factory
    elif ClasseEnum.SUMMONER.value == classe_name:
        class_skill_factory = summoner_skill_factory
    elif ClasseEnum.MERCENARY.value == classe_name:
        class_skill_factory = mercenary_skill_factory
    elif ClasseEnum.NECROMANCER.value == classe_name:
        class_skill_factory = necromancer_skill_factory
    elif ClasseEnum.RANGER.value == classe_name:
        class_skill_factory = ranger_skill_factory
    elif ClasseEnum.SHAMAN.value == classe_name:
        class_skill_factory = shaman_skill_factory
    elif ClasseEnum.BERSERKIR.value == classe_name:
        class_skill_factory = berserkir_skill_factory
    elif ClasseEnum.WEAPON_MASTER.value == classe_name:
        class_skill_factory = weapon_master_skill_factory
    elif ClasseEnum.SORCERER_SUPREME.value == classe_name:
        raise ValueError(f'skills factory pra {classe_name} não implementada!')
    elif ClasseEnum.LORD_OF_THE_ROGUES.value == classe_name:
        raise ValueError(f'skills factory pra {classe_name} não implementada!')
    elif ClasseEnum.SAMURAI.value == classe_name:
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
        return DRUID_SKILL_LIST
    elif ClasseEnum.SORCERER.value == classe_name:
        return SORCERER_SKILL_LIST
    elif ClasseEnum.WARRIOR.value == classe_name:
        return WARRIOR_SKILL_LIST
    elif ClasseEnum.ROGUE.value == classe_name:
        return ROGUE_SKILL_LIST
    elif ClasseEnum.MAGE.value == classe_name:
        return MAGE_SKILL_LIST
    elif ClasseEnum.PALADIN.value == classe_name:
        return PALADIN_SKILL_LIST
    elif ClasseEnum.GUARDIAN.value == classe_name:
        return GUARDIAN_SKILL_LIST
    elif ClasseEnum.DUELIST.value == classe_name:
        return DUELIST_SKILL_LIST
    elif ClasseEnum.HERALD.value == classe_name:
        return HERALD_SKILL_LIST
    elif ClasseEnum.ARCANIST.value == classe_name:
        return ARCANIST_SKILL_LIST
    elif ClasseEnum.BARD.value == classe_name:
        return BARD_SKILL_LIST
    elif ClasseEnum.BOUNTY_HUNTER.value == classe_name:
        return BOUNTY_HUNTER_SKILL_LIST
    elif ClasseEnum.KNIGHT.value == classe_name:
        return KNIGHT_SKILL_LIST
    elif ClasseEnum.HEALER.value == classe_name:
        return HEALER_SKILL_LIST
    elif ClasseEnum.GLADIATOR.value == classe_name:
        return GLADIATOR_SKILL_LIST
    elif ClasseEnum.SUMMONER.value == classe_name:
        return SUMMONER_SKILL_LIST
    elif ClasseEnum.MERCENARY.value == classe_name:
        return MERCENARY_SKILL_LIST
    elif ClasseEnum.NECROMANCER.value == classe_name:
        return NECROMANCER_SKILL_LIST
    elif ClasseEnum.RANGER.value == classe_name:
        return RANGER_SKILL_LIST
    elif ClasseEnum.SHAMAN.value == classe_name:
        return SHAMAN_SKILL_LIST
    elif ClasseEnum.BERSERKIR.value == classe_name:
        return BERSERKIR_SKILL_LIST
    elif ClasseEnum.WEAPON_MASTER.value == classe_name:
        return WEAPON_MASTER_SKILL_LIST
    elif ClasseEnum.SORCERER_SUPREME.value == classe_name:
        raise ValueError(f'skills para {classe_name} ainda não implementada!')
    elif ClasseEnum.LORD_OF_THE_ROGUES.value == classe_name:
        raise ValueError(f'skills para {classe_name} ainda não implementada!')
    elif ClasseEnum.SAMURAI.value == classe_name:
        raise ValueError(f'skills para {classe_name} ainda não implementada!')
    else:
        raise ValueError(f'Classe {classe_name} não encontrada!')
