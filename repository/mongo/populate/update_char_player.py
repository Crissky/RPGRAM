'''
Arquivo responsável por resetar os atributos base dos jogadores, 
além de atualizar os bônus dos atributos das raça e classe dos personagens.
O LEVEL do personagem será mantido. Os PONTOS DEVERÃO SER REDISTRIBUÍDOS.
'''
from repository.mongo import (
    RaceModel,
    ClasseModel,
    PlayerCharacterModel
)
from rpgram.characters import PlayerCharacter

if __name__ == "__main__":
    race_model = RaceModel()
    classe_model = ClasseModel()
    player_char_model = PlayerCharacterModel()
    player_chars = player_char_model.get_all()

    for player_char in player_chars:
        race_name = player_char.race.name
        classe_name = player_char.classe.name

        race = race_model.get(race_name)
        classe = classe_model.get(classe_name)

        player_id = player_char.player_id
        player_name = player_char.player_name
        char_name = player_char.name
        _id = player_char._id
        level = player_char.base_stats.level
        created_at = player_char.created_at
        updated_at = player_char.updated_at

        xp = player_char.base_stats.xp

        new_player_char = PlayerCharacter(
            player_id=player_id,
            player_name=player_name,
            char_name=char_name,
            _id=_id,
            race=race,
            classe=classe,
            level=level,
            xp=xp,
            created_at=created_at,
            updated_at=updated_at
        )
        player_char_model.save(new_player_char)
