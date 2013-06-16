from mamba import describe, before, skip
from sure import *
from doublex import *

from spec.constants import *

from simplecqrs.view_model import *

IRRELEVANT_INVENTORY_ITEM_DTO1 = 'irrelevant inventory item dto 1'
IRRELEVANT_INVENTORY_ITEM_DTO2 = 'irrelevant inventory item dto 2'

with describe('ReadModel') as _:

    def it_returns_all_the_inventory_items():
        _.db = Stub()
        _.read_model = ReadModel(_.db)
        dtos = [IRRELEVANT_INVENTORY_ITEM_DTO1, IRRELEVANT_INVENTORY_ITEM_DTO2]
        with _.db as db: db.inventory_items = dtos
        expect(_.read_model.get_inventory_items()).to.be.equal(dtos)

    @skip
    def it_returns_the_details_of_a_particular_inventory_item():
        pass
