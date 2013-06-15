from mamba import describe, context
from sure import *

class InMemoryDataBase(object):
    @property
    def inventory_items(self):
        return []

with describe('InMemoryDataBase') as _:

    with context('inventory items'):
        def it_starts_with_no_inventory_item_dtos():
            db = InMemoryDataBase()
            expect(db.inventory_items).to.be.empty

    with context('inventory item details'):
        pass
