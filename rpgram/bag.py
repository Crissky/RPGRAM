from datetime import datetime
from typing import List, Union

from bson import ObjectId
from constant.text import TEXT_DELIMITER
from function.text import escape_basic_markdown_v2, remove_bold, remove_code

from rpgram.boosters import Equipment
from rpgram.consumables.consumable import Consumable
from rpgram.item import Item
from rpgram.enums import EmojiEnum


ItemTypes = Union[Consumable, Equipment, Item]


class Bag:
    '''Classe que armazena os itens do jogador em formato de pacotes.
    Um pacote (Item) agrupa um tipo de item (Consumable, Equipment) fornecendo
    um conjunto de itens de mesmo tipo por meio da quantidade (quantity).'''

    def __init__(
        self,
        items: List[Item],
        player_id: int,
        _id: Union[str, ObjectId] = None,
        created_at: datetime = None,
        updated_at: datetime = None,
    ):
        if isinstance(_id, str):
            _id = ObjectId(_id)

        self.__items = []
        self.__player_id = player_id
        self.__id = _id
        self.__created_at = created_at
        self.__updated_at = updated_at
        for item in items:
            self.add(item)

    def pack_item(self, item: ItemTypes) -> Item:
        if isinstance(item, (Consumable, Equipment)):
            item = Item(item)
        if isinstance(item, Item):
            return item
        raise TypeError(f'Tipo esperado "{ItemTypes}", obtido "{type(item)}"')

    def get_item(self, item: ItemTypes = None, slot: int = None) -> ItemTypes:
        if item and item in self.__items:
            item_index = self.__items.index(item)
            return self.__items[item_index]
        elif isinstance(slot, int):
            return self.__items[slot]

    def add(self, item: ItemTypes) -> None:
        item = self.pack_item(item)
        bag_item = self.get_item(item)
        if bag_item:
            bag_item.quantity += item.quantity
        else:
            self.__items.append(item)

    def remove(
        self,
        item: ItemTypes = None,
        slot: int = None,
        quantity: int = 1
    ):
        if item:
            item = self.pack_item(item)
        bag_item = self.get_item(item, slot)
        if bag_item:
            bag_item.quantity -= quantity
        else:
            raise ValueError('Item não encontrado no Inventário.')

        if bag_item.quantity <= 0:
            self.__items.remove(bag_item)

    def sort_by_equip_type(self, reverse: bool = True):
        if reverse:  # Consumable first
            self.__items.sort(
                key=lambda x: (
                    -x.item_type_order,
                    -x.power,
                    -x.rarity_order,
                    -x.sell_price,
                    x.name,
                ), reverse=False
            )
        else:  # Equipment first
            self.__items.sort(
                key=lambda x: (
                    x.item_type_order,
                    -x.power,
                    -x.rarity_order,
                    -x.sell_price,
                    x.name,
                ), reverse=False
            )

    def sort_by_power(self, reverse: bool = True):
        if reverse:  # Greater power first
            self.__items.sort(
                key=lambda x: (
                    -x.power,
                    -x.item_type_order,
                    -x.rarity_order,
                    -x.sell_price,
                    x.name
                ), reverse=False
            )
        else:  # Lower power first
            self.__items.sort(
                key=lambda x: (
                    x.power,
                    -x.item_type_order,
                    -x.rarity_order,
                    -x.sell_price,
                    x.name
                ), reverse=False
            )

    def sort_by_rarity(self, reverse: bool = True):
        if reverse:  # More rare first
            self.__items.sort(
                key=lambda x: (
                    -x.rarity_order,
                    -x.power,
                    -x.item_type_order,
                    -x.sell_price,
                    x.name
                ), reverse=False
            )
        else:  # Less rare first
            self.__items.sort(
                key=lambda x: (
                    x.rarity_order,
                    -x.power,
                    -x.item_type_order,
                    -x.sell_price,
                    x.name
                ), reverse=False
            )

    def get_sheet(self, verbose: bool = False, markdown: bool = False) -> str:
        if verbose:
            text = '\n'.join([
                f'{item.quantity:02}x *{item.emoji_name}* '
                f'({item.weight:.2f}{EmojiEnum.WEIGHT.value})'
                for item in self.__items
            ])
        else:
            text = '\n'.join([
                f'{item.quantity:02}x *{item.name}*'
                for item in self.__items
            ])
        text += '\n'

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
            items_ids=[item.to_dict() for item in self.__items],
            player_id=self.__player_id,
            _id=self.__id,
            created_at=self.__created_at,
            updated_at=self.__updated_at,
        )

    def __getitem__(self, items: Union[int, slice]):
        if isinstance(items, (int, slice)):
            return self.__items[items]

    def __len__(self):
        return len(self.__items)

    # Getters
    @property
    def weight(self) -> float:
        return sum([item.weight for item in self.__items])

    @property
    def weight_text(self) -> float:
        return f'{self.weight:.2f}{EmojiEnum.WEIGHT.value}'

    @property
    def total_slots(self) -> int:
        return len(self.__items)

    _id = property(lambda self: self.__id)
    slots = total_slots


if __name__ == '__main__':
    from rpgram.enums import EquipmentEnum, DamageEnum, RarityEnum

    potion = Consumable(
        name='Potion',
        description='Cura 100 de HP.',
        weight=0.1,
        function='target.combat_stats.hp = 100',
        _id='111111111111111111111111',
    )
    high_potion = Consumable(
        name='High Potion',
        description='Cura 1000 de HP.',
        weight=0.1,
        function='target.combat_stats.hp = 1000',
        rarity=RarityEnum.UNCOMMON,
        _id='222222222222222222222222',
    )
    shield = Equipment(
        name='Escudo Comparativo de Madeira',
        equip_type=EquipmentEnum.ONE_HAND,
        damage_types=[DamageEnum.SLASHING, 'FIRE'],
        rarity=RarityEnum.RARE,
        _id='333333333333333333333333',
        bonus_physical_defense=10,
    )
    bag = Bag(
        items=[potion, potion, potion, high_potion, shield],
        player_id='ffffffffffffffffffffffff',
    )
    print(bag)
    bag.sort_by_equip_type()
    print(bag)
    bag.sort_by_power()
    print(bag)
    bag.sort_by_rarity()
    print(bag)
