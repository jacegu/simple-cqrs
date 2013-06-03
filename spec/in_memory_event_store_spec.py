from mamba import describe, context, before, skip
from sure import expect
from doublex import *

from spec.constants import *

from simplecqrs.persistence import InMemoryEventStore, AggregateNotFoundError, ConcurrencyError


with describe(InMemoryEventStore) as _:

    @before.each
    def create_event_store():
        _.publisher = Spy()
        _.event_store = InMemoryEventStore(_.publisher)

    with describe('saving events'):
        with context('when the provided version matches the expected one'):
            def it_saves_the_event():
                _.event_store.push(AGGREGATE_ID, IRRELEVANT_EVENT1, 0)
                _.event_store.push(AGGREGATE_ID, IRRELEVANT_EVENT2, 1)
                expect(_.event_store.get_events_for_aggregate(AGGREGATE_ID)). \
                  to.be.equal([IRRELEVANT_EVENT1, IRRELEVANT_EVENT2])

            def it_publishes_the_event():
                _.event_store.push(AGGREGATE_ID, IRRELEVANT_EVENT1, 0)
                assert_that(_.publisher.publish, called().with_args(IRRELEVANT_EVENT1))

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
