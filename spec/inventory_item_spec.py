from mamba import describe, before, context
from sure import expect

IRRELEVANT_ID = 'id'
IRRELEVANT_NAME = 'irrelevant name'
OTHER_NAME = 'other name'

class InventoryItemCreated(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def apply(self, inventory_item):
        inventory_item.id = self.id
        inventory_item.name = self.name
        inventory_item.active = True
        inventory_item.count = 0


class InventoryItemRenamed(object):
    def __init__(self, new_name):
        self.new_name = new_name

    def apply(self, inventory_item):
        inventory_item.name = self.new_name


class InventoryItemDeactivated(object):
    def apply(self, inventory_item):
        inventory_item.active = False


class ItemsCheckedInToInventory(object):
    def __init__(self, count):
        self.count = count

    def apply(self, inventory_item):
        inventory_item.count += self.count

class InvalidOperationError(RuntimeError):
    pass

class InventoryItem(object):
    def __init__(self, id, name):
        self.__applyChanges(InventoryItemCreated(id, name))

    def rename(self, new_name):
        if self.__invalid_name(new_name):
            raise ValueError("\"%s\" is not a valid Inventory Item name" % new_name)
        self.__applyChanges(InventoryItemRenamed(new_name))

    def deactivate(self):
        if self.is_inactive:
            raise InvalidOperationError("Cannot deactivate an inactive inventory item")
        self.__applyChanges(InventoryItemDeactivated())

    @property
    def is_active(self):
        return self.active

    @property
    def is_inactive(self):
        return not self.active

    def check_in(self, count):
        if count <= 0:
            raise InvalidOperationError('only 1 or more items can be checked in')
        self.__applyChanges(ItemsCheckedInToInventory(count))

    def remove(self, count):
        self.count -= count

    def __applyChanges(self, event):
        event.apply(self)

    def __invalid_name(self, name):
        return name is None or name == ''


with describe(InventoryItem) as _:

    @before.each
    def create_an_item():
        _.item = InventoryItem(IRRELEVANT_ID, IRRELEVANT_NAME)

    def it_has_an_id():
        expect(_.item.id).to.be.equal(IRRELEVANT_ID)

    def it_has_a_name():
        expect(_.item.name).to.be.equal(IRRELEVANT_NAME)

    def it_has_no_items():
        expect(_.item.count).to.equal(0)

    def it_is_active():
        expect(_.item.is_active).to.be.true

    with context('renaming'):
        def it_can_be_renamed_if_the_new_name_is_valid():
            _.item.rename(OTHER_NAME)
            expect(_.item.name).to.be.equal(OTHER_NAME)

        def it_cannot_be_renamed_if_the_new_name_is_invalid():
            expect(_.item.rename).when.called_with(None).to.throw(ValueError)
            expect(_.item.rename).when.called_with('').to.throw(ValueError)

    with context('deactivating'):
        def it_can_be_deactivated_when_active():
            _.item.deactivate()
            expect(_.item.is_active).to.be.false

        def it_cannot_be_deactivated_when_inactive():
            _.item.deactivate()
            expect(_.item.deactivate).when.called.to.throw(InvalidOperationError)

    with context('checking items in'):
        def it_can_check_in_one_or_more_items():
            _.item.check_in(8); _.item.check_in(12)
            expect(_.item.count).to.equal(20)

        def it_cannot_check_in_less_than_one_item():
            expect(_.item.check_in).when.called_with(0).to.throw(InvalidOperationError)

    with context('removing items'):
        def it_can_remove_one_or_more_items():
            _.item.check_in(5)
            _.item.remove(3)
            expect(_.item.count).to.be.equal(2)
