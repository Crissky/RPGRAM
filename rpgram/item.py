from typing import Union

from bson import ObjectId
from constant.text import TEXT_DELIMITER
from function.text import escape_basic_markdown_v2, remove_bold, remove_code

from rpgram.boosters.equipment import Equipment
from rpgram.consumables.consumable import Consumable
from rpgram.consumables.cure import CureConsumable
from rpgram.consumables.heal import HealingConsumable, ReviveConsumable
from rpgram.consumables.other import GemstoneConsumable, IdentifyingConsumable, TrocadoPouchConsumable, XPConsumable
from rpgram.enums.emojis import EmojiEnum
from rpgram.enums.equipment import EquipmentEnumOrder
from rpgram.enums.rarity import RarityEnum, RarityEnumOrder


ITEMS_TYPES = Union[Equipment, Consumable]
ITEMS_TYPES_TUPLE = (Equipment, Consumable)
SALABLE_ITEMS_TUPLE = (TrocadoPouchConsumable, GemstoneConsumable)


class Item:
    def __init__(self, item: ITEMS_TYPES, quantity: int = 1):
        if not isinstance(item, ITEMS_TYPES_TUPLE):
            raise TypeError(
                f'Item precisa ser de algum desses tipos: {ITEMS_TYPES_TUPLE}.\n'
                f'Mas o item fornecido é do tipo: ({type(item)}).'
            )

        self.item = item
        self.__quantity = 0
        self.quantity = quantity

    def add(self, quantity: int = 1) -> None:
        self.quantity += quantity

    def sub(self, quantity: int = 1) -> None:
        self.quantity -= quantity

    def use(self, target) -> dict:
        if self.quantity <= 0:
            raise ValueError(
                f'A quantidade de "{self.item.name}" é menor ou igual a zero.'
            )
        elif not isinstance(self.item, Consumable):
            raise TypeError(
                f'Item não é um consumível, é do tipo "{type(self.item)}".'
            )
        self.sub()

        return self.item.use(target=target)

    def battle_use(self, target) -> dict:
        if self.quantity >= 0:
            raise ValueError(f'Não possui "{self.item.name}".')
        elif not isinstance(self.item, Consumable):
            raise TypeError(
                f'Item não é um consumível, é do tipo "{type(self.item)}".'
            )
        self.sub()

        return self.item.battle_use(target=target)

    # Getters
    @property
    def _id(self) -> ObjectId:
        return self.item._id

    @property
    def name(self) -> str:
        return self.item.name

    @property
    def weight(self) -> float:
        return self.item.weight * self.quantity

    @property
    def quantity(self) -> int:
        return self.__quantity

    @property
    def power(self) -> int:
        power = 0
        if hasattr(self.item, 'power') and isinstance(self.item, Equipment):
            power = self.item.power

        return power

    @property
    def price(self) -> int:
        return self.item.price

    @property
    def sell_price(self) -> int:
        return self.item.sell_price

    @property
    def rarity(self) -> RarityEnum:
        return self.item.rarity

    @property
    def rarity_order(self) -> int:
        return RarityEnumOrder[self.rarity.name].value

    @property
    def item_type_order(self) -> int:
        if isinstance(self.item, Consumable):
            order = len(EquipmentEnumOrder)
            if isinstance(self.item, SALABLE_ITEMS_TUPLE):
                order += 1
            elif isinstance(self.item, IdentifyingConsumable):
                order += 2
            elif isinstance(self.item, XPConsumable):
                order += 3
            elif isinstance(self.item, CureConsumable):
                order += 4
            elif isinstance(self.item, ReviveConsumable):
                order += 5
            elif isinstance(self.item, HealingConsumable):
                order += 6
        elif isinstance(self.item, Equipment):
            order = EquipmentEnumOrder[self.item.equip_type.name].value

        return order

    @property
    def class_order(self) -> int:
        if isinstance(self.item, Consumable):
            order = 1
        elif isinstance(self.item, Equipment):
            order = 2

        return order

    # Setters
    @quantity.setter
    def quantity(self, value):
        quantity = self.__quantity
        self.__quantity = value
        if self.__quantity < 0:
            error_quantity = self.__quantity
            self.__quantity = quantity
            raise ValueError(
                f'Item não pode ter um valor negativo ({error_quantity}).'
            )

    def get_sheet(
        self,
        verbose: bool = False,
        markdown: bool = False,
        zero_fill: int = 2
    ) -> str:
        formated_quantity = f'{self.quantity}'.zfill(zero_fill)
        text = f'{formated_quantity}x {self.item.emoji_type}*{self.name}*'

        if verbose:
            if isinstance(self.item, Equipment):
                text += (
                    f' {self.item.power_and_level}'
                )
            elif isinstance(self.item, Consumable):
                text += f' ({self.weight:.2f}{EmojiEnum.WEIGHT.value})'
        text += f'\n'

        if not markdown:
            text = remove_bold(text)
            text = remove_code(text)
        else:
            text = escape_basic_markdown_v2(text)

        return text

    def get_all_sheets(
        self, verbose: bool = False,
        markdown: bool = False,
        show_quantity: bool = False,
    ) -> str:
        text = self.item.get_sheet(verbose=verbose, markdown=markdown)
        if all((verbose, show_quantity, isinstance(self.item, Consumable))):
            text_quantity = f'*Quantidade*: {self.quantity}\n'
            if not markdown:
                text_quantity = remove_bold(text_quantity)
                text_quantity = remove_code(text_quantity)
            else:
                text_quantity = escape_basic_markdown_v2(text_quantity)
            text += text_quantity
        return text

    def __repr__(self) -> str:
        return (
            f'{TEXT_DELIMITER}\n'
            f'{self.get_sheet(True)}'
            f'{TEXT_DELIMITER}\n'
        )

    def to_dict(self) -> dict:
        return dict(
            _id=self._id,
            quantity=self.quantity
        )

    def __eq__(self, other):
        if isinstance(other, Item):
            return self.item == other.item
        return self.item == other


if __name__ == '__main__':
    from rpgram.enums import DamageEnum, EquipmentEnum
    potion = Consumable(
        name='Potion',
        description='Cura 100 de HP.',
        weight=0.1,
    )
    sword = Equipment(
        name='Espada de Aço',
        equip_type=EquipmentEnum.ONE_HAND,
        damage_types=[DamageEnum.SLASHING, 'FIRE'],
        weight=15,
        requirements={'Nível': 1, 'FOR': 12},
        rarity='RARE',
    )
    item_potion = Item(potion, 5)
    item_sword = Item(sword, 2)
    print(item_sword)
    print(item_potion)
