from random import choice, randint
from typing import Union

from rpgram.enums.function import get_enum_by_index, get_enum_index
from rpgram.enums.rarity import RarityEnum


class SecretWordGame:
    _words = None
    _verbs = None
    _conjugations = None

    def __init__(self, rarity: Union[str, RarityEnum] = RarityEnum.COMMON):
        if isinstance(rarity, str):
            rarity = RarityEnum[rarity.upper()]

        if isinstance(rarity, RarityEnum):
            self.rarity = rarity
            self.size = 5 + get_enum_index(self.rarity) + randint(0, 2)
        else:
            raise TypeError(
                f'Rarity deve ser do tipo RarityEnum ou String. '
                f'Tipo: {type(rarity)}.'
            )

        self.secret_word = self.__get_secret_word()

    def __get_secret_word(self) -> str:
        options = self.options
        secret_word = choice([o for o in options if len(o) == self.size])
        return secret_word.upper()

    @classmethod
    def __get_words(cls):
        if cls._words is None:
            print('loading words')
            with open('rpgram/minigames/secret_word/dicio', 'r') as file:
                words = file.read()
                words = words.splitlines()
                cls._words = set(words)

        return cls._words.copy()

    @classmethod
    def __get_verbs(cls):
        if cls._verbs is None:
            print('loading verbs')
            with open('rpgram/minigames/secret_word/verbos', 'r') as file:
                verbs = file.read()
                verbs = verbs.splitlines()
                cls._verbs = set(verbs)

        return cls._verbs.copy()

    @classmethod
    def __get_conjugations(cls):
        if cls._conjugations is None:
            print('loading conjugations')
            with open('rpgram/minigames/secret_word/conjugações', 'r') as file:
                conjugations = file.read()
                conjugations = conjugations.splitlines()
                cls._conjugations = set(conjugations)

        return cls._conjugations.copy()

    @property
    def words(self) -> set:
        return SecretWordGame.__get_words()

    @property
    def verbs(self) -> set:
        return SecretWordGame.__get_verbs()

    @property
    def conjugations(self) -> set:
        return SecretWordGame.__get_conjugations()

    @property
    def options(self) -> set:
        return self.words - (self.conjugations - self.verbs)

    def __repr__(self):
        return (
            f'SecretWordGame<'
            f'size={self.size}, '
            f'rarity={self.rarity}, '
            f'word={self.secret_word}'
            '>'
        )


if __name__ == '__main__':
    game1 = SecretWordGame(rarity='legendary')
    game2 = SecretWordGame()

    print('words', len(game1.words))
    print('verbs', len(game1.verbs))
    print('conjugations', len(game1.conjugations))

    print('words', len(game2.words))
    print('verbs', len(game2.verbs))
    print('conjugations', len(game2.conjugations))

    print(game1)
    print(game2)
