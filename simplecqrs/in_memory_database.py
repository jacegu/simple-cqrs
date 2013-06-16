class InMemoryDatabase(object):
    def __init__(self):
        self.inventory_items_dtos = {}
        self.inventory_item_details_dtos = {}

    @property
    def inventory_items(self):
        return self.inventory_items_dtos.values()

    def add_inventory_item(self, inventory_item_dto):
        self.inventory_items_dtos[inventory_item_dto.id] = inventory_item_dto

    def remove_inventory_item(self, inventory_item_id):
        del(self.inventory_items_dtos[inventory_item_id])

    @property
    def inventory_item_details(self):
        return self.inventory_item_details_dtos.values()

    def add_inventory_item_details(self, inventory_item_details_dto):
        self.inventory_item_details_dtos[inventory_item_details_dto.id] = inventory_item_details_dto

    def remove_inventory_item_details(self, inventory_item_details_id):
        del(self.inventory_item_details_dtos[inventory_item_details_id])

    def get_inventory_item_details(self, inventory_item_details_id):
        return self.inventory_item_details_dtos[inventory_item_details_id]
