from mamba import describe, before, context
from sure import expect
from doublex import *
from hamcrest import instance_of

from spec.constants import *

from simplecqrs.aggregate import Aggregate


class DummyAggregate(Aggregate):
    def __init__(self):
        Aggregate.__init__(self)
        self.name = IRRELEVANT_NAME

    def change_name(self, new_name):
        self._apply_changes(DummyEvent(new_name))


class DummyAggregate2(Aggregate):
    def __init__(self):
        Aggregate.__init__(self)
        self.uncommitted_changes.append(IRRELEVANT_EVENT1)


class DummyEvent(object):
    def __init__(self, new_name):
        self.new_name = new_name

    def apply_changes(self, subject):
        subject.name = self.new_name


with describe('an example Aggregate') as _:

    @before.each
    def create_aggregate():
        _.aggregate = DummyAggregate()

    with context('creating aggregate from events'):
        def it_makes_sure_no_uncomitted_changes_exist():
            event = Spy()
            aggregate = DummyAggregate2.from_events([event])
            expect(aggregate.uncommitted_changes).to.be.empty

        def it_replays_every_event_on_a_new_aggregate_and_returns_it():
            event1 = Spy()
            event2 = Spy()
            DummyAggregate.from_events([event1, event2])
            assert_that(event1.apply_changes, called().with_args(instance_of(DummyAggregate)))
            assert_that(event2.apply_changes, called().with_args(instance_of(DummyAggregate)))

    with context('uncommitted changes'):
        def starts_with_no_none():
            expect(_.aggregate.uncommitted_changes).to.be.empty

        def holds_every_applied_change():
            _.aggregate.change_name(OTHER_NAME)
            expect(_.aggregate.uncommitted_changes).to.have.length_of(1)

        def gets_empty_once_changes_are_committed():
            _.aggregate.change_name(OTHER_NAME)
            _.aggregate.changes_committed()
            expect(_.aggregate.uncommitted_changes).to.be.empty

