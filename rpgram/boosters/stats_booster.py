from bson import ObjectId
from datetime import datetime
from typing import Union

from constant.text import SECTION_HEAD, TEXT_DELIMITER
from function.text import escape_basic_markdown_v2, remove_bold, remove_code


class StatsBooster:
    '''Classe Base para ser usada em características que dão bônus aos 
    atributos dos personagens como: Raça, Classe, Taletos, Equipamentos, etc.

    A princípio esses atributos não são alterados, permanencendo os mesmos 
    valores do momento de sua criação.

    '''

    def __init__(
        self,
        _id: Union[str, ObjectId] = None,
        bonus_strength: int = 0,
        bonus_dexterity: int = 0,
        bonus_constitution: int = 0,
        bonus_intelligence: int = 0,
        bonus_wisdom: int = 0,
        bonus_charisma: int = 0,
        multiplier_strength: float = 1.0,
        multiplier_dexterity: float = 1.0,
        multiplier_constitution: float = 1.0,
        multiplier_intelligence: float = 1.0,
        multiplier_wisdom: float = 1.0,
        multiplier_charisma: float = 1.0,
        bonus_hit_points: int = 0,
        bonus_initiative: int = 0,
        bonus_physical_attack: int = 0,
        bonus_precision_attack: int = 0,
        bonus_magical_attack: int = 0,
        bonus_physical_defense: int = 0,
        bonus_magical_defense: int = 0,
        bonus_hit: int = 0,
        bonus_evasion: int = 0,
        secret_bonus_strength: int = 0,
        secret_bonus_dexterity: int = 0,
        secret_bonus_constitution: int = 0,
        secret_bonus_intelligence: int = 0,
        secret_bonus_wisdom: int = 0,
        secret_bonus_charisma: int = 0,
        secret_multiplier_strength: float = 0.0,
        secret_multiplier_dexterity: float = 0.0,
        secret_multiplier_constitution: float = 0.0,
        secret_multiplier_intelligence: float = 0.0,
        secret_multiplier_wisdom: float = 0.0,
        secret_multiplier_charisma: float = 0.0,
        secret_bonus_hit_points: int = 0,
        secret_bonus_initiative: int = 0,
        secret_bonus_physical_attack: int = 0,
        secret_bonus_precision_attack: int = 0,
        secret_bonus_magical_attack: int = 0,
        secret_bonus_physical_defense: int = 0,
        secret_bonus_magical_defense: int = 0,
        secret_bonus_hit: int = 0,
        secret_bonus_evasion: int = 0,
        identified: bool = None,
        created_at: datetime = None,
        updated_at: datetime = None
    ) -> None:
        if isinstance(_id, str):
            _id = ObjectId(_id)

        self.__id = _id

        self.__bonus_strength = int(bonus_strength)
        self.__bonus_dexterity = int(bonus_dexterity)
        self.__bonus_constitution = int(bonus_constitution)
        self.__bonus_intelligence = int(bonus_intelligence)
        self.__bonus_wisdom = int(bonus_wisdom)
        self.__bonus_charisma = int(bonus_charisma)

        self.__multiplier_strength = float(multiplier_strength)
        self.__multiplier_dexterity = float(multiplier_dexterity)
        self.__multiplier_constitution = float(multiplier_constitution)
        self.__multiplier_intelligence = float(multiplier_intelligence)
        self.__multiplier_wisdom = float(multiplier_wisdom)
        self.__multiplier_charisma = float(multiplier_charisma)

        self.__bonus_hit_points = int(bonus_hit_points)
        self.__bonus_initiative = int(bonus_initiative)
        self.__bonus_physical_attack = int(bonus_physical_attack)
        self.__bonus_precision_attack = int(bonus_precision_attack)
        self.__bonus_magical_attack = int(bonus_magical_attack)
        self.__bonus_physical_defense = int(bonus_physical_defense)
        self.__bonus_magical_defense = int(bonus_magical_defense)
        self.__bonus_hit = int(bonus_hit)
        self.__bonus_evasion = int(bonus_evasion)

        self.__secret_bonus_strength = int(secret_bonus_strength)
        self.__secret_bonus_dexterity = int(secret_bonus_dexterity)
        self.__secret_bonus_constitution = int(secret_bonus_constitution)
        self.__secret_bonus_intelligence = int(secret_bonus_intelligence)
        self.__secret_bonus_wisdom = int(secret_bonus_wisdom)
        self.__secret_bonus_charisma = int(secret_bonus_charisma)

        self.__secret_multiplier_strength = float(
            secret_multiplier_strength
        )
        self.__secret_multiplier_dexterity = float(
            secret_multiplier_dexterity
        )
        self.__secret_multiplier_constitution = float(
            secret_multiplier_constitution
        )
        self.__secret_multiplier_intelligence = float(
            secret_multiplier_intelligence
        )
        self.__secret_multiplier_wisdom = float(
            secret_multiplier_wisdom
        )
        self.__secret_multiplier_charisma = float(
            secret_multiplier_charisma
        )

        self.__secret_bonus_hit_points = int(
            secret_bonus_hit_points
        )
        self.__secret_bonus_initiative = int(
            secret_bonus_initiative
        )
        self.__secret_bonus_physical_attack = int(
            secret_bonus_physical_attack
        )
        self.__secret_bonus_precision_attack = int(
            secret_bonus_precision_attack
        )
        self.__secret_bonus_magical_attack = int(
            secret_bonus_magical_attack
        )
        self.__secret_bonus_physical_defense = int(
            secret_bonus_physical_defense
        )
        self.__secret_bonus_magical_defense = int(
            secret_bonus_magical_defense
        )
        self.__secret_bonus_hit = int(
            secret_bonus_hit
        )
        self.__secret_bonus_evasion = int(
            secret_bonus_evasion
        )

        self.__identified = identified
        self.__created_at = created_at
        self.__updated_at = updated_at

    def get_sheet(self, verbose: bool = False, markdown: bool = False) -> str:
        text = ''

        if verbose:
            text += (
                f'*{SECTION_HEAD.format("BÔNUS E MULTIPLICADORES")}*\n'

                f'`FOR: {self.strength:+}'
                f'x({self.multiplier_strength:+.2f})`\n'
                f'`DES: {self.dexterity:+}'
                f'x({self.multiplier_dexterity:+.2f})`\n'
                f'`CON: {self.constitution:+}'
                f'x({self.multiplier_constitution:+.2f})`\n'
                f'`INT: {self.intelligence:+}'
                f'x({self.multiplier_intelligence:+.2f})`\n'
                f'`SAB: {self.wisdom:+}'
                f'x({self.multiplier_wisdom:+.2f})`\n'
                f'`CAR: {self.charisma:+}'
                f'x({self.multiplier_charisma:+.2f})`\n\n'

                f'`HP: {self.hp:+}`\n'
                f'`INICIATIVA: {self.initiative:+}`\n'
                f'`ATAQUE FÍSICO: {self.physical_attack:+}`\n'
                f'`ATAQUE DE PRECISÃO: {self.precision_attack:+}`\n'
                f'`ATAQUE MÁGICO: {self.magical_attack:+}`\n'
                f'`DEFESA FÍSICA: {self.physical_defense:+}`\n'
                f'`DEFESA MÁGICA: {self.magical_defense:+}`\n'
                f'`ACERTO: {self.hit:+}`\n'
                f'`EVASÃO: {self.evasion:+}`\n'
            )
            if self.__identified:
                text += (
                    f'*\n{SECTION_HEAD.format("BÔNUS IDENTIFICADOS")}*\n'
                )
                if self.__secret_bonus_strength:
                    text += f'`FOR: {self.__secret_bonus_strength:+}'
                    if self.__secret_multiplier_strength:
                        text += (
                            f'x('
                            f'{self.__secret_multiplier_strength:+.2f})'
                        )
                    text += f'`\n'
                if self.__secret_bonus_dexterity:
                    text += f'`DES: {self.__secret_bonus_dexterity:+}'
                    if self.__secret_multiplier_dexterity:
                        text += (
                            f'x('
                            f'{self.__secret_multiplier_dexterity:+.2f})'
                        )
                    text += '`\n'
                if self.__secret_bonus_constitution:
                    text += f'`CON: {self.__secret_bonus_constitution:+}'
                    if self.__secret_multiplier_constitution:
                        text += (
                            f'x('
                            f'{self.__secret_multiplier_constitution:+.2f})'
                        )
                    text += '`\n'
                if self.__secret_bonus_intelligence:
                    text += f'`INT: {self.__secret_bonus_intelligence:+}'
                    if self.__secret_multiplier_intelligence:
                        text += (
                            f'x('
                            f'{self.__secret_multiplier_intelligence:+.2f})'
                        )
                    text += '`\n'
                if self.__secret_bonus_wisdom:
                    text += f'`SAB: {self.__secret_bonus_wisdom:+}'
                    if self.__secret_multiplier_wisdom:
                        text += (
                            f'x('
                            f'{self.__secret_multiplier_wisdom:+.2f})'
                        )
                    text += '`\n'
                if self.__secret_bonus_charisma:
                    text += f'`CAR: {self.__secret_bonus_charisma:+}'
                    if self.__secret_multiplier_charisma:
                        text += (
                            f'x('
                            f'{self.__secret_multiplier_charisma:+.2f})'
                        )
                    text += '`\n\n'

                if text[-3:] != '`\n\n' and text[-2:] != '*\n':
                    text += '\n'

                if self.__secret_bonus_hit_points:
                    text += f'`HP: {self.__secret_bonus_hit_points:+}`\n'
                if self.__secret_bonus_initiative:
                    text += (
                        f'`INICIATIVA: {self.__secret_bonus_initiative:+}`\n'
                    )
                if self.__secret_bonus_physical_attack:
                    text += (
                        f'`ATAQUE FÍSICO: '
                        f'{self.__secret_bonus_physical_attack:+}`\n'
                    )
                if self.__secret_bonus_precision_attack:
                    text += (
                        f'`ATAQUE DE PRECISÃO: '
                        f'{self.__secret_bonus_precision_attack:+}`\n'
                    )
                if self.__secret_bonus_magical_attack:
                    text += (
                        f'`ATAQUE MÁGICO: '
                        f'{self.__secret_bonus_magical_attack:+}`\n'
                    )
                if self.__secret_bonus_physical_defense:
                    text += (
                        f'`DEFESA FÍSICA: '
                        f'{self.__secret_bonus_physical_defense:+}`\n'
                    )
                if self.__secret_bonus_magical_defense:
                    text += (
                        f'`DEFESA MÁGICA: '
                        f'{self.__secret_bonus_magical_defense:+}`\n'
                    )
                if self.__secret_bonus_hit:
                    text += f'`ACERTO: {self.__secret_bonus_hit:+}`\n'
                if self.__secret_bonus_evasion:
                    text += f'`EVASÃO: {self.__secret_bonus_evasion:+}`\n'

        if not markdown:
            text = remove_bold(text)
            text = remove_code(text)
        else:
            text = escape_basic_markdown_v2(text)

        return text

    def get_all_sheets(
        self, verbose: bool = False, markdown: bool = False
    ) -> str:
        return self.get_sheet(verbose=verbose, markdown=markdown)

    def __repr__(self) -> str:
        return (
            f'{TEXT_DELIMITER}\n'
            f'{self.get_sheet(True)}'
            f'{TEXT_DELIMITER}\n'
        )

    def to_dict(self):
        return dict(
            _id=self.__id,
            bonus_strength=self.__bonus_strength,
            bonus_dexterity=self.__bonus_dexterity,
            bonus_constitution=self.__bonus_constitution,
            bonus_intelligence=self.__bonus_intelligence,
            bonus_wisdom=self.__bonus_wisdom,
            bonus_charisma=self.__bonus_charisma,
            multiplier_strength=self.__multiplier_strength,
            multiplier_dexterity=self.__multiplier_dexterity,
            multiplier_constitution=self.__multiplier_constitution,
            multiplier_intelligence=self.__multiplier_intelligence,
            multiplier_wisdom=self.__multiplier_wisdom,
            multiplier_charisma=self.__multiplier_charisma,
            bonus_hit_points=self.__bonus_hit_points,
            bonus_initiative=self.__bonus_initiative,
            bonus_physical_attack=self.__bonus_physical_attack,
            bonus_precision_attack=self.__bonus_precision_attack,
            bonus_magical_attack=self.__bonus_magical_attack,
            bonus_physical_defense=self.__bonus_physical_defense,
            bonus_magical_defense=self.__bonus_magical_defense,
            bonus_hit=self.__bonus_hit,
            bonus_evasion=self.__bonus_evasion,
            secret_bonus_strength=self.__secret_bonus_strength,
            secret_bonus_dexterity=self.__secret_bonus_dexterity,
            secret_bonus_constitution=self.__secret_bonus_constitution,
            secret_bonus_intelligence=self.__secret_bonus_intelligence,
            secret_bonus_wisdom=self.__secret_bonus_wisdom,
            secret_bonus_charisma=self.__secret_bonus_charisma,
            secret_multiplier_strength=self.__secret_multiplier_strength,
            secret_multiplier_dexterity=self.__secret_multiplier_dexterity,
            secret_multiplier_constitution=self.__secret_multiplier_constitution,
            secret_multiplier_intelligence=self.__secret_multiplier_intelligence,
            secret_multiplier_wisdom=self.__secret_multiplier_wisdom,
            secret_multiplier_charisma=self.__secret_multiplier_charisma,
            secret_bonus_hit_points=self.__secret_bonus_hit_points,
            secret_bonus_initiative=self.__secret_bonus_initiative,
            secret_bonus_physical_attack=self.__secret_bonus_physical_attack,
            secret_bonus_precision_attack=self.__secret_bonus_precision_attack,
            secret_bonus_magical_attack=self.__secret_bonus_magical_attack,
            secret_bonus_physical_defense=self.__secret_bonus_physical_defense,
            secret_bonus_magical_defense=self.__secret_bonus_magical_defense,
            secret_bonus_hit=self.__secret_bonus_hit,
            secret_bonus_evasion=self.__secret_bonus_evasion,
            identified=self.__identified,
            created_at=self.__created_at,
            updated_at=self.__updated_at,
        )

    # Getters
    @property
    def bonus_strength(self):
        value = self.__bonus_strength
        if self.__identified:
            value += self.__secret_bonus_strength
        return value

    @property
    def bonus_dexterity(self):
        value = self.__bonus_dexterity
        if self.__identified:
            value += self.__secret_bonus_dexterity
        return value

    @property
    def bonus_constitution(self):
        value = self.__bonus_constitution
        if self.__identified:
            value += self.__secret_bonus_constitution
        return value

    @property
    def bonus_intelligence(self):
        value = self.__bonus_intelligence
        if self.__identified:
            value += self.__secret_bonus_intelligence
        return value

    @property
    def bonus_wisdom(self):
        value = self.__bonus_wisdom
        if self.__identified:
            value += self.__secret_bonus_wisdom
        return value

    @property
    def bonus_charisma(self):
        value = self.__bonus_charisma
        if self.__identified:
            value += self.__secret_bonus_charisma
        return value

    @property
    def multiplier_strength(self):
        value = self.__multiplier_strength
        if self.__identified:
            value += self.__secret_multiplier_strength
        return value

    @property
    def multiplier_dexterity(self):
        value = self.__multiplier_dexterity
        if self.__identified:
            value += self.__secret_multiplier_dexterity
        return value

    @property
    def multiplier_constitution(self):
        value = self.__multiplier_constitution
        if self.__identified:
            value += self.__secret_multiplier_constitution
        return value

    @property
    def multiplier_intelligence(self):
        value = self.__multiplier_intelligence
        if self.__identified:
            value += self.__secret_multiplier_intelligence
        return value

    @property
    def multiplier_wisdom(self):
        value = self.__multiplier_wisdom
        if self.__identified:
            value += self.__secret_multiplier_wisdom
        return value

    @property
    def multiplier_charisma(self):
        value = self.__multiplier_charisma
        if self.__identified:
            value += self.__secret_multiplier_charisma
        return value

    @property
    def bonus_hit_points(self):
        value = self.__bonus_hit_points
        if self.__identified:
            value += self.__secret_bonus_hit_points
        return value

    @property
    def bonus_initiative(self):
        value = self.__bonus_initiative
        if self.__identified:
            value += self.__secret_bonus_initiative
        return value

    @property
    def bonus_physical_attack(self):
        value = self.__bonus_physical_attack
        if self.__identified:
            value += self.__secret_bonus_physical_attack
        return value

    @property
    def bonus_precision_attack(self):
        value = self.__bonus_precision_attack
        if self.__identified:
            value += self.__secret_bonus_precision_attack
        return value

    @property
    def bonus_magical_attack(self):
        value = self.__bonus_magical_attack
        if self.__identified:
            value += self.__secret_bonus_magical_attack
        return value

    @property
    def bonus_physical_defense(self):
        value = self.__bonus_physical_defense
        if self.__identified:
            value += self.__secret_bonus_physical_defense
        return value

    @property
    def bonus_magical_defense(self):
        value = self.__bonus_magical_defense
        if self.__identified:
            value += self.__secret_bonus_magical_defense
        return value

    @property
    def bonus_hit(self):
        value = self.__bonus_hit
        if self.__identified:
            value += self.__secret_bonus_hit
        return value

    @property
    def bonus_evasion(self):
        value = self.__bonus_evasion
        if self.__identified:
            value += self.__secret_bonus_evasion
        return value

    @property
    def identifiable(self):
        '''Retorna True se o objeto puder ser identificado.
        Retorna False se o objeto não puder (ou já foi) ser identificado'''
        if self.__identified is None or self.__identified is True:
            return False
        elif self.__identified is False:
            return True

    _id = property(lambda self: self.__id)
    strength = bonus_strength
    dexterity = bonus_dexterity
    constitution = bonus_constitution
    intelligence = bonus_intelligence
    wisdom = bonus_wisdom
    charisma = bonus_charisma
    hp = hit_points = bonus_hit_points
    initiative = bonus_initiative
    physical_attack = bonus_physical_attack
    precision_attack = bonus_precision_attack
    magical_attack = bonus_magical_attack
    physical_defense = bonus_physical_defense
    magical_defense = bonus_magical_defense
    hit = bonus_hit
    evasion = bonus_evasion
    created_at = property(lambda self: self.__created_at)
    updated_at = property(lambda self: self.__updated_at)


if __name__ == '__main__':
    bonus_stats = StatsBooster(
        _id='ffffffffffffffffffffffff',
        bonus_strength=10,
        bonus_dexterity=11,
        bonus_constitution=12,
        bonus_intelligence=13,
        bonus_wisdom=14,
        bonus_charisma=15,
        multiplier_strength=1.6,
        multiplier_dexterity=1.7,
        multiplier_constitution=1.8,
        multiplier_intelligence=-1.9,
        multiplier_wisdom=2.0,
        multiplier_charisma=-2.1,
        bonus_hit_points=220,
        bonus_initiative=23,
        bonus_physical_attack=24,
        bonus_precision_attack=25,
        bonus_magical_attack=-26,
        bonus_physical_defense=27,
        bonus_magical_defense=-28,
        bonus_hit=29,
        bonus_evasion=30,
        identified=True,
        secret_bonus_strength=31,
        secret_bonus_dexterity=32,
        secret_bonus_constitution=33,
        secret_bonus_intelligence=34,
        secret_bonus_wisdom=35,
        secret_bonus_charisma=-36,
        secret_multiplier_strength=37,
        secret_multiplier_dexterity=38,
        secret_multiplier_constitution=39,
        secret_multiplier_intelligence=40,
        secret_multiplier_wisdom=41,
        secret_multiplier_charisma=42,
        secret_bonus_hit_points=143,
        secret_bonus_initiative=44,
        secret_bonus_physical_attack=45,
        secret_bonus_precision_attack=46,
        secret_bonus_magical_attack=47,
        secret_bonus_physical_defense=48,
        secret_bonus_magical_defense=49,
        secret_bonus_hit=50,
        secret_bonus_evasion=51,
    )
    print(bonus_stats)
    print(bonus_stats.to_dict())
