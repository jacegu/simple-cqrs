from mamba import describe, before
from sure import expect

IRRELEVANT_ID = 'id'
IRRELEVANT_NAME = 'irrelevant name'

class InventoryItem(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name

with describe(InventoryItem) as _:

     def it_has_an_id():
        item = InventoryItem(IRRELEVANT_ID, IRRELEVANT_NAME)
        expect(item.id).to.be.equal(IRRELEVANT_ID)

     def it_has_a_name():
        item = InventoryItem(IRRELEVANT_ID, IRRELEVANT_NAME)
        expect(item.name).to.be.equal(IRRELEVANT_NAME)
