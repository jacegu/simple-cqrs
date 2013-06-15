from mamba import describe, context, before, skip
from sure import *

from spec.constants import *


class InMemoryDataBase(object):
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


with describe('InMemoryDataBase') as _:

    @before.each
    def create_db():
        _.db = InMemoryDataBase()

    with context('inventory items'):
        def it_starts_with_no_inventory_item_dtos():
            expect(_.db.inventory_items).to.be.empty

        def it_can_add_inventory_items():
            _.db.add_inventory_item(InventoryItemDto(IRRELEVANT_ID, IRRELEVANT_NAME))
            expect(_.db.inventory_items).to.have.length_of(1)

        def it_can_list_all_inventory_items():
            dto1 = InventoryItemDto(OTHER_ID, OTHER_NAME)
            dto2 = InventoryItemDto(IRRELEVANT_ID, IRRELEVANT_NAME)
            _.db.add_inventory_item(dto1)
            _.db.add_inventory_item(dto2)
            expect(_.db.inventory_items).to.be.equal([dto1, dto2])

        def it_can_remove_a_particular_item():
            dto1 = InventoryItemDto(OTHER_ID, OTHER_NAME)
            _.db.add_inventory_item(dto1)
            _.db.remove_inventory_item(OTHER_ID)
            expect(_.db.inventory_items).to.be.empty

    with context('inventory item details'):
        @before.each
        def create_dto():
            _.dto = InventoryItemDetailsDto(IRRELEVANT_ID, IRRELEVANT_NAME, \
                                            IRRELEVANT_COUNT, IRRELEVANT_VERSION)

        def it_starts_with_no_inventory_item_details():
            expect(_.db.inventory_item_details).to.be.empty

        def it_can_add_new_inventory_item_details():
            _.db.add_inventory_item_details(_.dto)
            expect(_.db.inventory_item_details).to.be.equal([_.dto])

        def it_can_remove_inventory_item_details():
            _.db.add_inventory_item_details(_.dto)
            _.db.remove_inventory_item_details(IRRELEVANT_ID)
            expect(_.db.inventory_item_details).to.be.empty

        def it_can_get_inventory_item_details_by_id():
            _.db.add_inventory_item_details(_.dto)
            expect(_.db.get_inventory_item_details(IRRELEVANT_ID)).to.be.equal(_.dto)
