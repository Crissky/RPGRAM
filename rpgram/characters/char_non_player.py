from datetime import datetime
from bson import ObjectId
from rpgram.boosters.classe import Classe
from rpgram.boosters.race import Race
from rpgram.characters.char_base import BaseCharacter
from rpgram.enums.enemy import EnemyStarsEnum
from rpgram.equips import Equips
from rpgram.status import Status


POINTS_MULTIPLIER = {
    EnemyStarsEnum.ONE.name: 2,
    EnemyStarsEnum.TWO.name: 3,
    EnemyStarsEnum.THREE.name: 5,
    EnemyStarsEnum.FOUR.name: 7,
    EnemyStarsEnum.FIVE.name: 11,
    EnemyStarsEnum.BOSS.name: 28,
}


class NPCharacter(BaseCharacter):
    def __init__(
        self,
        char_name: str,
        classe: Classe,
        race: Race,
        enemy_id: ObjectId = None,
        equips: Equips = None,
        status: Status = None,
        level: int = 1,
        xp: int = 0,
        base_strength: int = 0,
        base_dexterity: int = 0,
        base_constitution: int = 0,
        base_intelligence: int = 0,
        base_wisdom: int = 0,
        base_charisma: int = 0,
        stars: str = EnemyStarsEnum.THREE.name,
        combat_damage: int = 0,
        _id: ObjectId = None,
        created_at: datetime = None,
        updated_at: datetime = None
    ) -> None:
        points_multiplier = POINTS_MULTIPLIER[stars]
        super().__init__(
            char_name=char_name,
            classe=classe,
            race=race,
            player_id=enemy_id,
            equips=equips,
            status=status,
            level=level,
            xp=xp,
            base_strength=base_strength,
            base_dexterity=base_dexterity,
            base_constitution=base_constitution,
            base_intelligence=base_intelligence,
            base_wisdom=base_wisdom,
            base_charisma=base_charisma,
            points_multiplier=points_multiplier,
            combat_damage=combat_damage,
            _id=_id,
            created_at=created_at,
            updated_at=updated_at
        )
        self.__stars = stars

    # Getters
    @property
    def name(self) -> str:
        return super().name + f'({self.emoji_stars})'

    @property
    def stars(self) -> int:
        return self.__stars

    @property
    def emoji_stars(self):
        return EnemyStarsEnum[self.stars].value

    @property
    def enemy_id(self) -> ObjectId:
        return super().player_id
