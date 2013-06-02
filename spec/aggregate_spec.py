from mamba import describe, before, context
from sure import expect

from simplecqrs.aggregate import Aggregate

IRRELEVANT_NAME = 'irrelevant name'
OTHER_NAME = 'other name'

class DummyAggregate(Aggregate):
    def __init__(self):
        Aggregate.__init__(self)
        self.name = IRRELEVANT_NAME

    def change_name(self, new_name):
        self._apply_changes(DummyEvent(new_name))


class DummyEvent(object):
    def __init__(self, new_name):
        self.new_name = new_name

    def apply_changes(self, subject):
        subject.name = self.new_name


with describe('an example Aggregate') as _:

    @before.each
    def create_aggregate():
        _.aggregate = DummyAggregate()

    with context('uncommitted changes'):
        def starts_with_no_none():
            expect(_.aggregate.uncommitted_changes).to.be.empty

        def holds_every_applied_change():
            _.aggregate.change_name(OTHER_NAME)
            expect(_.aggregate.uncommitted_changes).to.have.length_of(1)
