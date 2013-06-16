from mamba import describe, before, skip
from sure import *
from doublex import *

from spec.constants import *

from simplecqrs.view_model import *

IRRELEVANT_INVENTORY_ITEM_DTO1 = 'irrelevant inventory item dto 1'
IRRELEVANT_INVENTORY_ITEM_DTO2 = 'irrelevant inventory item dto 2'
IRRELEVANT_INVENTORY_ITEM_DETAILS_DTO = 'irrelevant inventory item details dto'

class ReadModel(object):
    def __init__(self, database):
        self.database = database

    def get_inventory_items(self):
        return self.database.inventory_items


with describe('ReadModel') as _:

    @before.each
    def creat_read_model():
        _.db = Stub()
        _.read_model = ReadModel(_.db)

    def it_returns_all_the_inventory_items():
        dtos = [IRRELEVANT_INVENTORY_ITEM_DTO1, IRRELEVANT_INVENTORY_ITEM_DTO2]
        with _.db as db: db.inventory_items = dtos
        expect(_.read_model.get_inventory_items()).to.be.equal(dtos)

    def it_returns_the_details_of_a_particular_inventory_item():
        dto = IRRELEVANT_INVENTORY_ITEM_DETAILS_DTO
        with _.db as db: 
            db.get_inventory_item_details(IRRELEVANT_ID).returns(dto)
        expect(_.read_model.get_inventory_item_details(IRRELEVANT_ID)).to.be.equal(dto)
