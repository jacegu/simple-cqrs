from mamba import describe, context, before
from sure import *
from doublex import *
from hamcrest import instance_of

from spec.constants import *

from simplecqrs.persistence import Repository
from simplecqrs.inventory import InventoryItem
from simplecqrs.commands import *
from contextlib import contextmanager

class InventoryCommandsHandler(object):
    def __init__(self, inventory_item_repository):
        self.inventory_item_repository = inventory_item_repository

    def handle(self, command):
        #FIXME: Replace conditional with polymorphism of some kind.
        #       Probably the best choice is to create individual handlers for each command type.
        #       Pushing the handle command to each class is another possibility. The handle
        #       method would receive the repository as a parameter. I am not sure about it though.
        if command.__class__ == CreateInventoryItem:
            self.inventory_item_repository.save(InventoryItem(command.item_id, command.item_name))
        if command.__class__ == RenameInventoryItem:
            with self._inventory_item(command.item_id, command.original_version) as item:
                item.rename(command.new_item_name)
        if command.__class__ == DeactivateInventoryItem:
            with self._inventory_item(command.item_id, command.original_version) as item:
                item.deactivate()
        if command.__class__ == CheckInItemsToInventory:
            with self._inventory_item(command.item_id, command.original_version) as item:
                item.check_in(command.item_count)
        if command.__class__ == RemoveItemsFromInventory:
            with self._inventory_item(command.item_id, command.original_version) as item:
                item.remove(command.item_count)


    @contextmanager
    def _inventory_item(self, item_id, item_version):
        item = self.inventory_item_repository.find_by_id(item_id)
        yield item
        self.inventory_item_repository.save(item, item_version)


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
