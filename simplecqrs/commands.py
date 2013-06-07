class CreateInventoryItem(object):
    def __init__(self, item_id, item_name):
        self.item_id = item_id
        self.item_name = item_name


class RenameInventoryItem(object):
    def __init__(self, item_id, new_item_name, original_version):
        self.item_id = item_id
        self.new_item_name = new_item_name
        self.original_version = original_version


class DeactivateInventoryItem(object):
     def __init__(self, item_id, original_version):
        self.item_id = item_id
        self.original_version = original_version


class CheckInItemsToInventory(object):
     def __init__(self, item_id, item_count, original_version):
        self.item_id = item_id
        self.item_count = item_count
        self.original_version = original_version


class RemoveItemsFromInventory(object):
     def __init__(self, item_id, item_count, original_version):
        self.item_id = item_id
        self.item_count = item_count
        self.original_version = original_version
