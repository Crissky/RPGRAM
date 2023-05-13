from datetime import datetime
from bson import ObjectId
from rpgram.boosters import Race, Classe
from rpgram.characters import BaseCharacter
from rpgram.stats import BaseStats, CombatStats


class PlayerCharacter(BaseCharacter):
    def __init__(
        self,
        player_id: int,
        player_name: str,
        char_name: str,
        _id: ObjectId = None,
        base_stats: BaseStats = None,
        combat_stats: CombatStats = None,
        classe: Classe = None,
        race: Race = None,
        level: int = 1,
        base_strength: int = 0,
        base_dexterity: int = 0,
        base_constitution: int = 0,
        base_intelligence: int = 0,
        base_wisdom: int = 0,
        base_charisma: int = 0,
        race_name: str = '',
        race_description: str = '',
        race_bonus_strength: int = 0,
        race_bonus_dexterity: int = 0,
        race_bonus_constitution: int = 0,
        race_bonus_intelligence: int = 0,
        race_bonus_wisdom: int = 0,
        race_bonus_charisma: int = 0,
        race_multiplier_strength: float = 1.0,
        race_multiplier_dexterity: float = 1.0,
        race_multiplier_constitution: float = 1.0,
        race_multiplier_intelligence: float = 1.0,
        race_multiplier_wisdom: float = 1.0,
        race_multiplier_charisma: float = 1.0,
        classe_name: str = '',
        classe_description: str = '',
        classe_bonus_strength: int = 0,
        classe_bonus_dexterity: int = 0,
        classe_bonus_constitution: int = 0,
        classe_bonus_intelligence: int = 0,
        classe_bonus_wisdom: int = 0,
        classe_bonus_charisma: int = 0,
        classe_multiplier_strength: float = 1.0,
        classe_multiplier_dexterity: float = 1.0,
        classe_multiplier_constitution: float = 1.0,
        classe_multiplier_intelligence: float = 1.0,
        classe_multiplier_wisdom: float = 1.0,
        classe_multiplier_charisma: float = 1.0,
        created_at: datetime = None,
        updated_at: datetime = None
    ) -> None:
        super().__init__(
            char_name=char_name,
            _id=_id,
            base_stats=base_stats,
            combat_stats=combat_stats,
            classe=classe,
            race=race,
            level=level,
            base_strength=base_strength,
            base_dexterity=base_dexterity,
            base_constitution=base_constitution,
            base_intelligence=base_intelligence,
            base_wisdom=base_wisdom,
            base_charisma=base_charisma,
            race_name=race_name,
            race_description=race_description,
            race_bonus_strength=race_bonus_strength,
            race_bonus_dexterity=race_bonus_dexterity,
            race_bonus_constitution=race_bonus_constitution,
            race_bonus_intelligence=race_bonus_intelligence,
            race_bonus_wisdom=race_bonus_wisdom,
            race_bonus_charisma=race_bonus_charisma,
            race_multiplier_strength=race_multiplier_strength,
            race_multiplier_dexterity=race_multiplier_dexterity,
            race_multiplier_constitution=race_multiplier_constitution,
            race_multiplier_intelligence=race_multiplier_intelligence,
            race_multiplier_wisdom=race_multiplier_wisdom,
            race_multiplier_charisma=race_multiplier_charisma,
            classe_name=classe_name,
            classe_description=classe_description,
            classe_bonus_strength=classe_bonus_strength,
            classe_bonus_dexterity=classe_bonus_dexterity,
            classe_bonus_constitution=classe_bonus_constitution,
            classe_bonus_intelligence=classe_bonus_intelligence,
            classe_bonus_wisdom=classe_bonus_wisdom,
            classe_bonus_charisma=classe_bonus_charisma,
            classe_multiplier_strength=classe_multiplier_strength,
            classe_multiplier_dexterity=classe_multiplier_dexterity,
            classe_multiplier_constitution=classe_multiplier_constitution,
            classe_multiplier_intelligence=classe_multiplier_intelligence,
            classe_multiplier_wisdom=classe_multiplier_wisdom,
            classe_multiplier_charisma=classe_multiplier_charisma,
            created_at=created_at,
            updated_at=updated_at
        )
        self.__player_id = player_id
        self.__player_name = player_name

    player_id = property(lambda self: self.__player_id)
    player_name = property(lambda self: self.__player_name)

    def get_sheet(self):
        return (
            f'Jogador: {self.player_name}\n'
            f'ID do Jogador: {self.player_id}\n'
            f'{super().get_sheet()}'
        )

    def to_dict(self):
        _dict = {'player_id': self.player_id, 'player_name': self.player_name}
        _dict.update(super().to_dict())

        return _dict


if __name__ == '__main__':
    player_character = PlayerCharacter(
        player_id=10,
        player_name='Jogador Teste',
        char_name='Personagem Jogador Teste',
        _id='ffffffffffffffffffffffff',
        level=21,
        base_strength=10,
        base_dexterity=10,
        base_constitution=10,
        base_intelligence=10,
        base_wisdom=10,
        base_charisma=10,
        race_name='Anão',
        race_description='Anão Teste do Jogador',
        race_bonus_strength=10,
        race_bonus_dexterity=8,
        race_bonus_constitution=14,
        race_bonus_intelligence=10,
        race_bonus_wisdom=10,
        race_bonus_charisma=8,
        race_multiplier_strength=1.0,
        race_multiplier_dexterity=1.0,
        race_multiplier_constitution=1.4,
        race_multiplier_intelligence=1.0,
        race_multiplier_wisdom=1.0,
        race_multiplier_charisma=1.0,
        classe_name='Bárbaro',
        classe_description='Bárbaro Teste de jogador',
        classe_bonus_strength=18,
        classe_bonus_dexterity=12,
        classe_bonus_constitution=15,
        classe_bonus_intelligence=5,
        classe_bonus_wisdom=5,
        classe_bonus_charisma=5,
        classe_multiplier_strength=2,
        classe_multiplier_dexterity=1.0,
        classe_multiplier_constitution=1.5,
        classe_multiplier_intelligence=0.5,
        classe_multiplier_wisdom=1,
        classe_multiplier_charisma=0.5,
    )
    print(player_character)
    print(player_character.to_dict())
