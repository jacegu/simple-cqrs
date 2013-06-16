from mamba import describe, before, skip
from sure import *
from doublex import *

from spec.constants import *
from simplecqrs.read_model import InventoryItemDto
from simplecqrs.events import InventoryItemCreated
from simplecqrs.in_memory_database import InMemoryDatabase



with describe('InventoryListView') as _:

    def it_handles_inventory_item_created_events():
        _.db = Stub(InMemoryDatabase)
        _.view = InventoryListView(_.db)
        event = InventoryItemCreated(IRRELEVANT_ID, IRRELEVANT_NAME)
        _.view.handle(event)
        assert_that(_.db.add_inventory_item, called().with_args(InventoryItemDto(IRRELEVANT_ID, IRRELEVANT_NAME)))

    @skip
    def it_handles_inventory_item_renamed_events():
        pass

    @skip
    def it_handles_inventory_item_deactivated_events():
        pass
