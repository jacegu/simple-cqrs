from mamba import describe, context
from sure import *

from spec.constants import *

class InMemoryDataBase(object):
    def __init__(self):
        self.inventory_item_dtos = []

    @property
    def inventory_items(self):
        return self.inventory_item_dtos

    def add(self, inventory_item_dto):
        self.inventory_item_dtos.append(inventory_item_dto)

class InventoryItemDto(object):
    def __init__(self, id, name):
        pass

with describe('InMemoryDataBase') as _:

    with context('inventory items'):
        def it_starts_with_no_inventory_item_dtos():
            db = InMemoryDataBase()
            expect(db.inventory_items).to.be.empty

        def it_can_add_inventory_item_dtos():
            db = InMemoryDataBase()
            db.add(InventoryItemDto(IRRELEVANT_ID, IRRELEVANT_NAME))
            expect(db.inventory_items).to.have.length_of(1)

    with context('inventory item details'):
        pass
