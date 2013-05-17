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


class InventoryItemRenamed(object):
    def __init__(self, new_name):
        self.new_name = new_name

    def apply(self, inventory_item):
        inventory_item.name = self.new_name


class InventoryItemDeactivated(object):
    def apply(self, inventory_item):
        inventory_item.active = False


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

    with context('renaming'):
        def it_can_be_renamed_if_the_new_name_is_valid():
            _.item.rename(OTHER_NAME)
            expect(_.item.name).to.be.equal(OTHER_NAME)

        def it_cannot_be_renamed_if_the_new_name_is_invalid():
            expect(_.item.rename).when.called_with(None).to.throw(ValueError)
            expect(_.item.rename).when.called_with('').to.throw(ValueError)

    with context('deactivating'):
        def it_starts_active():
            expect(_.item.is_active).to.be.true

        def it_can_be_deactivated_when_active():
            _.item.deactivate()
            expect(_.item.is_active).to.be.false

        def it_cannot_be_deactivated_when_inactive():
            _.item.deactivate()
            expect(_.item.deactivate).when.called.to.throw(InvalidOperationError)
