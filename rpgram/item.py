from typing import Union
from constant.text import TEXT_DELIMITER
from function.text import escape_basic_markdown_v2, remove_bold, remove_code

from rpgram.boosters import Equipment
from rpgram import Consumable

ItemsTypes = Union[Equipment, Consumable]


class Item:
    def __init__(self, item: ItemsTypes, quantity: int = 1):
        self.item = item
        self.__quantity = 0
        self.quantity = quantity

    # Getters
    @property
    def name(self):
        return self.item.name

    @property
    def weight(self):
        return self.item.weight * self.quantity

    @property
    def quantity(self):
        return self.__quantity

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

    def get_sheet(self, verbose: bool = False, markdown: bool = False) -> str:
        text = f'{self.quantity:02}x *{self.name}*'

        if verbose:
            text += f' ({self.weight}w)'
        # text += f'\n'

        if not markdown:
            text = remove_bold(text)
            text = remove_code(text)
        else:
            text = escape_basic_markdown_v2(text)

        return text

    def get_all_sheets(
        self, verbose: bool = False, markdown: bool = False
    ) -> str:
        return self.item.get_sheet(verbose=verbose, markdown=markdown)

    def __repr__(self) -> str:
        return f'{self.get_sheet(True)}'

    def to_dict(self):
        return dict(
            item=self.item._id,
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
        function='target.combat_stats.hp = 100'
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
