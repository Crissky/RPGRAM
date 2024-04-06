from datetime import datetime
from typing import Union
from bson import ObjectId
from function.text import escape_basic_markdown_v2, remove_bold, remove_code
from rpgram.boosters.classe import Classe
from rpgram.boosters.race import Race
from rpgram.characters.char_base import BaseCharacter
from rpgram.constants.text import ALIGNMENT_EMOJI_TEXT
from rpgram.enums.emojis import EmojiEnum
from rpgram.enums.enemy import AlignmentEnum, EnemyStarsEnum
from rpgram.equips import Equips
from rpgram.status import Status


POINTS_MULTIPLIER = {
    EnemyStarsEnum.ONE.name: 1,
    EnemyStarsEnum.TWO.name: 2,
    EnemyStarsEnum.THREE.name: 3,
    EnemyStarsEnum.FOUR.name: 5,
    EnemyStarsEnum.FIVE.name: 7,
    EnemyStarsEnum.BOSS.name: 11,
}


class NPCharacter(BaseCharacter):
    def __init__(
        self,
        char_name: str,
        classe: Classe,
        race: Race,
        alignment: Union[AlignmentEnum, str],
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
        stars: Union[EnemyStarsEnum, str] = EnemyStarsEnum.THREE,
        combat_damage: int = 0,
        _id: ObjectId = None,
        created_at: datetime = None,
        updated_at: datetime = None
    ) -> None:
        if isinstance(alignment, str):
            alignment = AlignmentEnum[alignment]
        elif not isinstance(alignment, AlignmentEnum):
            raise ValueError(
                f'alignment precisa ser uma string ou AlignmentEnum.'
            )

        if isinstance(stars, str):
            stars = EnemyStarsEnum[stars]
        elif not isinstance(stars, EnemyStarsEnum):
            raise ValueError(
                f'stars precisa ser uma string ou EnemyStarsEnum.'
            )

        points_multiplier = POINTS_MULTIPLIER[stars.name]

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

        self.__alignment = alignment
        self.__stars = stars

    # Getters
    @property
    def name(self) -> str:
        return super().name + f'({self.emoji_stars})'

    @property
    def player_name(self) -> str:
        return super().player_name + f'({self.emoji_stars})'
    
    @property
    def alignment(self) -> AlignmentEnum:
        return self.__alignment

    @property
    def alignment_name(self) -> str:
        return self.__alignment.value

    @property
    def stars(self) -> EnemyStarsEnum:
        return self.__stars

    @property
    def emoji_stars(self):
        return self.stars.value

    @property
    def enemy_id(self) -> ObjectId:
        return super().player_id

    def get_sheet(self, verbose: bool = False, markdown: bool = False) -> str:
        text = f'*{ALIGNMENT_EMOJI_TEXT}*: {self.alignment_name}\n'

        if not markdown:
            text = remove_bold(text)
            text = remove_code(text)
        else:
            text = escape_basic_markdown_v2(text)

        text += f'{super().get_sheet(verbose, markdown)}'

        return text

    def to_dict(self):
        _dict = {
            'alignment': self.alignment.name,
            'stars': self.stars.name
        }
        _dict.update(super().to_dict())

        return _dict
