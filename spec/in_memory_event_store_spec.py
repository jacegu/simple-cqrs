from mamba import describe, context, before, skip
from sure import expect

from spec.constants import *


class InMemoryEventStore(object):
    def __init__(self):
        self.events = {}

    def save(self, aggregate_id, events, version):
        self.events[aggregate_id] = events

    def get_events_for_aggregate(self, aggregate_id):
        if aggregate_id in self.events:
            return self.events[aggregate_id]
        else:
            raise AggregateNotFoundError()


class AggregateNotFoundError(RuntimeError):
    pass


with describe(InMemoryEventStore) as _:

    @before.each
    def create_event_store():
        _.event_store = InMemoryEventStore()

    with describe('saving events'):
        with context('when the provided version matches the expected one'):
            @skip
            def it_saves_the_event():
                aggregate_id, aggregate_version = IRRELEVANT_ID, 0
                _.event_store.push(aggregate_id, IRRELEVANT_EVENT, aggregate_version)
                expect(_.event_store.get_events_for_aggregate(aggregate_id)).to.be.equal([IRRELEVANT_EVENT])

            @skip
            def it_publishes_the_event():
                pass

        with context('when the provided version is different from the expected one'):
            @skip
            def it_raises_a_concurrency_error():
                pass

    with describe('getting events for an aggregate'):
        with context('when the aggregate is found'):
            def it_returns_the_aggregates_events():
                aggregate_id = IRRELEVANT_ID
                _.event_store.save(aggregate_id, IRRELEVANT_EVENT, IRRELEVANT_VERSION)
                expect(_.event_store.get_events_for_aggregate(aggregate_id)).to.be.equal(IRRELEVANT_EVENT)

        with context('when no aggregate with provided id is found'):
            def it_raises_an_aggregate_not_found_exception():
                expect(_.event_store.get_events_for_aggregate). \
                  when.called_with(IRRELEVANT_ID).to.throw(AggregateNotFoundError)
