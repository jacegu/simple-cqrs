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
