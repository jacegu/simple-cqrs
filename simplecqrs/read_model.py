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
