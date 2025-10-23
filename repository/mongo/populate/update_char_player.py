'''
Arquivo responsável por resetar os atributos base dos jogadores,
além de atualizar os bônus dos atributos das raça e classe dos personagens.
O LEVEL do personagem será mantido. Os PONTOS DEVERÃO SER REDISTRIBUÍDOS.
'''
from repository.mongo import (
    RaceModel,
    ClasseModel,
    CharacterModel
)
from rpgram.characters import PlayerCharacter

if __name__ == "__main__":
    race_model = RaceModel()
    classe_model = ClasseModel()
    char_model = CharacterModel()
    player_chars = char_model.get_all()

    for player_char in player_chars:
        player_char.base_stats.reset_stats()
        dict_char = player_char.to_dict()

        new_player_char = PlayerCharacter(**dict_char)
        char_model.save(new_player_char)
