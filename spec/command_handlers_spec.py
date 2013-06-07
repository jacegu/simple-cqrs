from mamba import describe, context
from sure import *
from doublex import *
from hamcrest import instance_of

from spec.constants import *

from simplecqrs.persistence import Repository
from simplecqrs.inventory import InventoryItem
from simplecqrs.commands import *


class InventoryCommandsHandler(object):
    def __init__(self, inventory_item_repository):
        self.inventory_item_repository = inventory_item_repository

    def handle(self, command):
        self.inventory_item_repository.save(InventoryItem(command.item_id, command.item_name))


with describe('InventoryCommandsHandler') as _:

    def it_can_handle_a_create_inventory_item_command():
        _.repository = Spy(Repository)
        _.handler = InventoryCommandsHandler(_.repository)
        command = CreateInventoryItem(IRRELEVANT_ID, IRRELEVANT_NAME)

        _.handler.handle(command)

        assert_that(_.repository.save, called().with_args(instance_of(InventoryItem)))
