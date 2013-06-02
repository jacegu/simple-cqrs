from mamba import describe, before, context
from sure import expect

from simplecqrs.inventory import InventoryItem, InvalidOperationError

IRRELEVANT_ID = 'id'
IRRELEVANT_NAME = 'irrelevant name'
OTHER_NAME = 'other name'

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
            expect(_.item.check_in).when.called_with(-1).to.throw(InvalidOperationError)

    with context('removing items'):
        def it_can_remove_one_or_more_items():
            _.item.check_in(5)
            _.item.remove(3)
            expect(_.item.count).to.be.equal(2)

        def it_cannot_remove_less_than_one_item():
            expect(_.item.remove).when.called_with(0).to.throw(InvalidOperationError)
            expect(_.item.remove).when.called_with(-1).to.throw(InvalidOperationError)

    with context('behaving like an aggregate'):
        def it_stores_its_uncommitted_changes():
            expect(_.item.uncommitted_changes).to.be.empty()
            _.item.deactivate()
            expect(_.item.uncommitted_changes).to.have.length_of(1)
