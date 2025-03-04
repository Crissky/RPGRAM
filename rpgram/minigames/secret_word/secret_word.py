import pandas as pd
import re
import unicodedata

from pathlib import Path
from random import choices
from typing import Union

from rpgram.enums.function import get_enum_index
from rpgram.enums.rarity import RarityEnum
from rpgram.errors import InvalidWordError


WORD_FILEPATH = Path('rpgram/minigames/secret_word/files')
MIN_WORD_SIZE = 5
MAX_GAME_WORD_LIST_LENGTH = 100


class SecretWordGame:
    _df = None
    _words = None
    _clean_words = None
    _verbs = None
    _conjugations = None
    _last_words = {}

    def __init__(self, rarity: Union[str, RarityEnum] = RarityEnum.COMMON):
        if isinstance(rarity, str):
            rarity = RarityEnum[rarity.upper()]

        if isinstance(rarity, RarityEnum):
            self.rarity = rarity
            self.size = MIN_WORD_SIZE + get_enum_index(self.rarity)
            self.secret_word = self.__get_secret_word()
            self.num_try = 0
            self.word_list = []
            self.check_list = []
            self.letter_set = set()
        else:
            raise TypeError(
                f'Rarity deve ser do tipo RarityEnum ou String. '
                f'Tipo: {type(rarity)}.'
            )

    def check_word(self, word: str) -> dict:
        clean_word = SecretWordGame.clear_word(word)
        clean_secret_word = SecretWordGame.clear_word(self.secret_word)
        size = len(clean_secret_word)

        if len(clean_word) != size:
            raise InvalidWordError(f'Palavra deve ter {size} letras.')
        elif clean_word not in self.clean_words:
            raise InvalidWordError(
                f'"{word.upper()}" não é uma palavra válida.'
            )

        check = ['⬛'] * size
        letters = list(clean_secret_word)
        for i in range(size):
            if clean_word[i] == clean_secret_word[i]:
                check[i] = '🟩'
                letters[i] = None
                self.letter_set.add(clean_word[i])

        for i in range(size):
            if check[i] == '🟩':
                continue
            if clean_word[i] in letters:
                check[i] = '🟨'
                letters[letters.index(clean_word[i])] = None
                self.letter_set.add(clean_word[i])

        check_text = ''.join(check)
        result_secret_word = self.secret_word.upper()
        result_word = word.upper()
        self.check_list.append(check_text)
        self.word_list.append(result_word)
        check_list = self.check_list.copy()
        word_list = self.word_list.copy()
        letter_set = self.letter_set.copy()
        is_correct = check == ['🟩'] * size
        if not is_correct:
            self.num_try += 1

        text = ''
        for check, word in zip(check_list, word_list):
            text += (
                f'`{" ".join(word)}`\n'
                f'`{check}`\n\n'
            )
        text += 'Letras na palavra: '
        text += ', '.join(sorted(letter_set)).upper()
        text += '\n'
        result = {
            'check': check,
            'check_list': check_list,
            'is_correct': is_correct,
            'secret_word': result_secret_word,
            'text': text,
            'word': result_word,
            'word_list': word_list,
            'letter_set': letter_set
        }

        return result

    def add_last_game_word(self, word: str):
        word_list = self.last_game_word_list
        if word not in word_list:
            word_list.append(word)
        SecretWordGame._last_words[self.size] = (
            word_list[-MAX_GAME_WORD_LIST_LENGTH:]
        )

    def __get_secret_word(self) -> str:
        options = self.data.palavra.to_list()
        weights = self.data.tf.to_list()
        secret_word = choices(options, weights=weights)[0]
        self.add_last_game_word(secret_word)

        return secret_word

    @classmethod
    def clear_word(cls, word):
        normalized_word = re.sub(r'\W|\d', '', word)
        normalized_word = unicodedata.normalize('NFD', normalized_word)
        normalized_word = normalized_word.encode('ascii', 'ignore')
        normalized_word = normalized_word.decode('utf-8')
        normalized_word = normalized_word.upper()
        normalized_word = normalized_word.strip()

        return normalized_word

    @classmethod
    def __get_data(cls) -> pd.DataFrame:
        if cls._df is None:
            print('loading data...')
            conjugations = SecretWordGame.__get_conjugations()
            verbs = SecretWordGame.__get_verbs()
            cls._df = pd.read_csv(WORD_FILEPATH / 'data')
            cls._df = cls._df[cls._df.palavra.str.len() >= MIN_WORD_SIZE]
            cls._df = cls._df[~cls._df.isin((conjugations - verbs))]

        return cls._df.copy()

    @classmethod
    def __get_words(cls) -> set:
        if cls._words is None:
            print('loading words...')
            df = pd.read_csv(WORD_FILEPATH / 'data')
            cls._words = set(df.palavra)

        return cls._words.copy()

    @classmethod
    def __get_clean_words(cls) -> set:
        if cls._clean_words is None:
            print('loading clean words...')
            cls._clean_words = map(
                SecretWordGame.clear_word,
                SecretWordGame.__get_words()
            )
            cls._clean_words = set(cls._clean_words)

        return cls._clean_words.copy()

    @classmethod
    def __get_verbs(cls) -> set:
        if cls._verbs is None:
            print('loading verbs...')
            df = pd.read_csv(WORD_FILEPATH / 'verbos', names=['palavra'])
            cls._verbs = set(df.palavra)

        return cls._verbs.copy()

    @classmethod
    def __get_conjugations(cls) -> set:
        if cls._conjugations is None:
            print('loading conjugations...')
            df = pd.read_csv(WORD_FILEPATH / 'conjugações', names=['palavra'])
            cls._conjugations = set(df.palavra)

        return cls._conjugations.copy()

    @property
    def data(self) -> pd.DataFrame:
        df = SecretWordGame.__get_data()
        df = df[df.palavra.str.len() == self.size]
        df = df[~df.palavra.isin(self.last_game_word_list)]

        return df
    df = data

    @property
    def words(self) -> set:
        return SecretWordGame.__get_words()

    @property
    def clean_words(self) -> set:
        return SecretWordGame.__get_clean_words()

    @property
    def verbs(self) -> set:
        return SecretWordGame.__get_verbs()

    @property
    def conjugations(self) -> set:
        return SecretWordGame.__get_conjugations()

    @property
    def last_game_word_list(self) -> list:
        return SecretWordGame._last_words.get(self.size, [])

    def __repr__(self):
        return (
            f'SecretWordGame('
            f'size={self.size}, '
            f'rarity={self.rarity}, '
            f'num_try={self.num_try}, '
            f'word={self.secret_word}, '
            f'last_game_word_list={self.last_game_word_list}'
            f')'
        )


if __name__ == '__main__':
    [SecretWordGame() for _ in range(10)]
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

    game2.size = 5
    game2.secret_word = 'risão'
    print(game2.check_word('raios'))
    print(game2.check_word('risao'))
    print(game2.check_word('risão'))

    game2.size = 5
    game2.secret_word = 'false'
    print('MUDA PALAVRA PARA "FALSE"')
    print(game2.check_word('false'))

    print('CAIDO' in game2.clean_words, 'caído' in game2.words)
