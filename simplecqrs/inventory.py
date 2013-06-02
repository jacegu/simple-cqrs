from simplecqrs.aggregate import Aggregate

class InventoryItem(Aggregate):
    def __init__(self, id, name):
        Aggregate.__init__(self)
        self._apply_changes(InventoryItemCreated(id, name))

    def rename(self, new_name):
        if self.__invalid_name(new_name):
            raise ValueError("\"%s\" is not a valid Inventory Item name" % new_name)
        self._apply_changes(InventoryItemRenamed(new_name))

    def deactivate(self):
        if self.is_inactive:
            raise InvalidOperationError("Cannot deactivate an inactive inventory item")
        self._apply_changes(InventoryItemDeactivated())

    @property
    def is_active(self):
        return self.active

    @property
    def is_inactive(self):
        return not self.active

    def check_in(self, count):
        if count <= 0:
            raise InvalidOperationError('only 1 or more items can be checked in')
        self._apply_changes(ItemsCheckedInToInventory(count))

    def remove(self, count):
        if count <= 0:
            raise InvalidOperationError('only 1 or more items can be removed')
        self._apply_changes(ItemsRemovedFromInventory(count))

    def __invalid_name(self, name):
        return name is None or name == ''


class InventoryItemCreated(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def apply_changes(self, inventory_item):
        inventory_item.id = self.id
        inventory_item.name = self.name
        inventory_item.active = True
        inventory_item.count = 0


class InventoryItemRenamed(object):
    def __init__(self, new_name):
        self.new_name = new_name

    def apply_changes(self, inventory_item):
        inventory_item.name = self.new_name


class InventoryItemDeactivated(object):
    def apply_changes(self, inventory_item):
        inventory_item.active = False


class ItemsCheckedInToInventory(object):
    def __init__(self, count):
        self.count = count

    def apply_changes(self, inventory_item):
        inventory_item.count += self.count


class ItemsRemovedFromInventory(object):
    def __init__(self, count):
        self.count = count

    def apply_changes(self, inventory_item):
        inventory_item.count -= self.count


class InvalidOperationError(RuntimeError):
    pass
