from mamba import describe, before
from sure import expect

IRRELEVANT_NAME = 'irrelevant name'

with describe(InventoryItem) as _:

     def it_has_a_name():
        item = InventoryItem(IRRELEVANT_NAME)
        expect(item.name).to.be.equal(IRRELEVANT_NAME)
