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
        classe: Classe,
        race: Race,
        level: int = 1,
        xp: int = 0,
        base_strength: int = 0,
        base_dexterity: int = 0,
        base_constitution: int = 0,
        base_intelligence: int = 0,
        base_wisdom: int = 0,
        base_charisma: int = 0,
        combat_damage: int = 0,
        _id: ObjectId = None,
        created_at: datetime = None,
        updated_at: datetime = None
    ) -> None:
        super().__init__(
            char_name=char_name,
            classe=classe,
            race=race,
            level=level,
            xp=xp,
            base_strength=base_strength,
            base_dexterity=base_dexterity,
            base_constitution=base_constitution,
            base_intelligence=base_intelligence,
            base_wisdom=base_wisdom,
            base_charisma=base_charisma,
            combat_damage=combat_damage,
            _id=_id,
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
