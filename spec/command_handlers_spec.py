from mamba import describe, context
from sure import *
from doublex import *
from hamcrest import instance_of

from spec.constants import *

from simplecqrs.persistence import Repository
from simplecqrs.inventory import InventoryItem
from simplecqrs.commands import *

with describe('InventoryCommandsHandler') as _:

    def it_can_handle_a_create_inventory_item_command():
        _.repository = Spy(Repository)
        _.handler = InventoryCommandsHandler(_.repository)
        command = CreateInventoryItem(IRRELEVANT_ID, IRRELEVANT_NAME)

        _.handler.handle(command)

        assert_that(_.repository.save, called().with_args(instance_of(InventoryItem)))
