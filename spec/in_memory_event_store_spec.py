from mamba import describe, context, before, skip
from sure import expect

from spec.constants import *


class InMemoryEventStore(object):
    def __init__(self):
        self.events = {}

    def push(self, aggregate_id, event, version):
        if aggregate_id in self.events:
            self._verify_version(aggregate_id, version)
        self._store(aggregate_id, event, version)

    def get_events_for_aggregate(self, aggregate_id):
        if aggregate_id in self.events:
            return [event_data['event'] for event_data in self.events[aggregate_id]]
        else:
            raise AggregateNotFoundError()

    def _verify_version(self, aggregate_id, provided_version):
        if provided_version != self._next_version_of(aggregate_id):
            raise ConcurrencyError()

    def _next_version_of(self, aggregate_id):
        return self.events.get(aggregate_id)[-1].get('version') + 1

    def _store(self, aggregate_id, event, version):
        self.events.setdefault(aggregate_id, []).append({'event': event, 'version': version})


class AggregateNotFoundError(RuntimeError):
    pass

class ConcurrencyError(RuntimeError):
    pass


with describe(InMemoryEventStore) as _:

    @before.each
    def create_event_store():
        _.event_store = InMemoryEventStore()

    with describe('saving events'):
        with context('when the provided version matches the expected one'):
            def it_saves_the_event():
                _.event_store.push(AGGREGATE_ID, IRRELEVANT_EVENT1, 0)
                _.event_store.push(AGGREGATE_ID, IRRELEVANT_EVENT2, 1)
                expect(_.event_store.get_events_for_aggregate(AGGREGATE_ID)). \
                  to.be.equal([IRRELEVANT_EVENT1, IRRELEVANT_EVENT2])

            @skip
            def it_publishes_the_event():
                pass

        with context('when the provided version is different from the expected one'):
            def it_raises_a_concurrency_error():
                _.event_store.push(AGGREGATE_ID, IRRELEVANT_EVENT, 0)
                expect(_.event_store.push).when. \
                  called_with(AGGREGATE_ID, IRRELEVANT_EVENT, 0).to.throw(ConcurrencyError)

    with describe('getting events for an aggregate'):
        with context('when the aggregate is found'):
            def it_returns_the_aggregates_events():
                _.event_store.push(AGGREGATE_ID, IRRELEVANT_EVENT, IRRELEVANT_VERSION)
                expect(_.event_store.get_events_for_aggregate(AGGREGATE_ID)).to.be.equal([IRRELEVANT_EVENT])

        with context('when no aggregate with provided id is found'):
            def it_raises_an_aggregate_not_found_exception():
                expect(_.event_store.get_events_for_aggregate). \
                  when.called_with(IRRELEVANT_ID).to.throw(AggregateNotFoundError)
