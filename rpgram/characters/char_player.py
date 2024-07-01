from datetime import datetime
from bson import ObjectId
from function.text import escape_basic_markdown_v2, remove_bold, remove_code

from rpgram.boosters.classe import Classe
from rpgram.boosters.race import Race
from rpgram.characters.char_base import BaseCharacter
from rpgram.constants.text import PLAYER_EMOJI_TEXT
from rpgram.equips import Equips
from rpgram.status import Status


class PlayerCharacter(BaseCharacter):
    def __init__(
        self,
        player_id: int,
        player_name: str,
        char_name: str,
        classe: Classe,
        race: Race,
        equips: Equips = None,
        status: Status = {},
        level: int = 1,
        xp: int = 0,
        base_strength: int = 0,
        base_dexterity: int = 0,
        base_constitution: int = 0,
        base_intelligence: int = 0,
        base_wisdom: int = 0,
        base_charisma: int = 0,
        points_multiplier: int = 3,
        combat_damage: int = 0,
        combat_death_counter: int = 0,
        skill_tree: dict = {},
        _id: ObjectId = None,
        created_at: datetime = None,
        updated_at: datetime = None
    ) -> None:
        super().__init__(
            char_name=char_name,
            classe=classe,
            race=race,
            player_id=player_id,
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
            combat_death_counter=combat_death_counter,
            skill_tree=skill_tree,
            _id=_id,
            created_at=created_at,
            updated_at=updated_at
        )
        self.__player_id = player_id
        self.__player_name = player_name

    def update_player_name(self, new_name: str):
        if not isinstance(new_name, str):
            raise TypeError('new_name precisa ser uma string')

        self.__player_name = new_name

    # Getters
    player_id: int = property(lambda self: self.__player_id)
    player_name: str = property(lambda self: self.__player_name)
    is_enemy: bool = property(lambda self: False)

    def get_sheet(self, verbose: bool = False, markdown: bool = False) -> str:
        text = f'*{PLAYER_EMOJI_TEXT}*: {self.player_name}\n'
        if verbose:
            text += f'*ID do Jogador*: {self.player_id}\n\n'

        if not markdown:
            text = remove_bold(text)
            text = remove_code(text)
        else:
            text = escape_basic_markdown_v2(text)

        text += f'{super().get_sheet(verbose, markdown)}'

        return text

    def get_all_sheets(
        self, verbose: bool = False, markdown: bool = False
    ) -> str:
        return f'{super().get_all_sheets(verbose, markdown)}'

    def to_dict(self):
        _dict = {'player_id': self.player_id, 'player_name': self.player_name}
        _dict.update(super().to_dict())

        return _dict


if __name__ == '__main__':
    classe = Classe(
        name='Bárbaro',
        description='Bárbaro Teste de jogador',
        bonus_strength=18,
        bonus_dexterity=12,
        bonus_constitution=15,
        bonus_intelligence=5,
        bonus_wisdom=5,
        bonus_charisma=5,
        multiplier_strength=2,
        multiplier_dexterity=1.0,
        multiplier_constitution=1.5,
        multiplier_intelligence=0.5,
        multiplier_wisdom=1,
        multiplier_charisma=0.5,
    )
    race = Race(
        name='Anão',
        description='Anão Teste do Jogador',
        bonus_strength=10,
        bonus_dexterity=8,
        bonus_constitution=14,
        bonus_intelligence=10,
        bonus_wisdom=10,
        bonus_charisma=8,
        multiplier_strength=1.0,
        multiplier_dexterity=1.0,
        multiplier_constitution=1.4,
        multiplier_intelligence=1.0,
        multiplier_wisdom=1.0,
        multiplier_charisma=1.0,
    )
    player_character = PlayerCharacter(
        player_id=10,
        player_name='Jogador Teste',
        char_name='Personagem Jogador Teste',
        classe=classe,
        race=race,
        _id='ffffffffffffffffffffffff',
        level=21,
        xp=500,
        base_strength=10,
        base_dexterity=10,
        base_constitution=10,
        base_intelligence=10,
        base_wisdom=10,
        base_charisma=10,
        combat_damage=300,
    )
    print(player_character)
    print(player_character.to_dict())
