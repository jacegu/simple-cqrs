class ReadModel(object):
    def __init__(self, database):
        self.database = database

    def get_inventory_items(self):
        return self.database.inventory_items

    def get_inventory_item_details(self, id):
        return self.database.get_inventory_item_details(id)


class InventoryItemDto(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name


class InventoryItemDetailsDto(object):
    def __init__(self, id, name, count, version):
        self.id = id
        self.name = name
        self.count = count
        self.version = version
