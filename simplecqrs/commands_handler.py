from contextlib import contextmanager

from simplecqrs.inventory import InventoryItem
from simplecqrs.commands import *

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
