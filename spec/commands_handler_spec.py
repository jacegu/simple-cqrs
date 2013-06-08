from mamba import describe, context, before
from sure import *
from doublex import *
from hamcrest import instance_of
from contextlib import contextmanager

from spec.constants import *
from simplecqrs.persistence import Repository
from simplecqrs.inventory import InventoryItem
from simplecqrs.commands import *

from simplecqrs.commands_handler import InventoryCommandsHandler


with describe('InventoryCommandsHandler') as _:

    @before.each
    def create_handler():
        _.repository = Spy(Repository)
        _.handler = InventoryCommandsHandler(_.repository)

    def it_can_handle_a_create_inventory_item_command():
        _.handler.handle(CreateInventoryItem(IRRELEVANT_ID, IRRELEVANT_NAME))
        assert_that(_.repository.save, called().with_args(instance_of(InventoryItem)))

    def it_can_handle_rename_inventory_item_commands():
        with _stubbed_item() as item:
            _.handler.handle(RenameInventoryItem(IRRELEVANT_ID, IRRELEVANT_NAME, IRRELEVANT_VERSION))
            assert_that(item.rename, called().with_args(IRRELEVANT_NAME))

    def it_can_handle_deactivate_inventory_item_commands():
        with _stubbed_item() as item:
            _.handler.handle(DeactivateInventoryItem(IRRELEVANT_ID, IRRELEVANT_VERSION))
            assert_that(item.deactivate, called())

    def it_can_handle_check_in_items_to_inventory_commands():
        with _stubbed_item() as item:
            _.handler.handle(CheckInItemsToInventory(IRRELEVANT_ID, IRRELEVANT_COUNT, IRRELEVANT_VERSION))
            assert_that(item.check_in, called().with_args(IRRELEVANT_COUNT))

    def it_can_handle_remove_items_from_inventory_commands():
        with _stubbed_item() as item:
            _.handler.handle(RemoveItemsFromInventory(IRRELEVANT_ID, IRRELEVANT_COUNT, IRRELEVANT_VERSION))
            assert_that(item.remove, called().with_args(IRRELEVANT_COUNT))

    @contextmanager
    def _stubbed_item():
        item = Spy(InventoryItem)
        with _.repository as r: r.find_by_id(IRRELEVANT_ID).returns(item)
        yield item
        assert_that(_.repository.save, called().with_args(item, IRRELEVANT_VERSION))
