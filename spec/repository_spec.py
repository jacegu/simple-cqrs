from mamba import describe, context, before
from doublex import *
from sure import expect

from spec.constants import *

from simplecqrs.persistence import Repository
from simplecqrs.aggregate import Aggregate

CHANGES = [IRRELEVANT_CHANGE1, IRRELEVANT_CHANGE2]

with describe(Repository) as _:

    @before.each
    def create_repository():
        _.storage = Spy()
        _.aggregate_class = Spy()
        _.repository = Repository(_.aggregate_class, _.storage)

    @before.each
    def create_aggregate():
        _.aggregate = Spy(Aggregate)
        _.aggregate.id = IRRELEVANT_ID
        _.aggregate.uncommitted_changes = CHANGES

    with context('saving an aggregate'):
        def it_saves_all_uncommited_changes():
            _.repository.save(_.aggregate)
            assert_that(_.storage.push, called().with_args(IRRELEVANT_ID, IRRELEVANT_CHANGE1))
            assert_that(_.storage.push, called().with_args(IRRELEVANT_ID, IRRELEVANT_CHANGE2))

        def it_marks_the_changes_as_committed():
            _.repository.save(_.aggregate)
            assert_that(_.aggregate.changes_committed, called())

    with context('finding an aggregate by id'):
        def it_returns_the_aggregate():
            with _.storage: _.storage.get_aggregate_changes(IRRELEVANT_ID).returns(CHANGES)
            with _.aggregate_class as klass: klass.from_events(CHANGES).returns(_.aggregate)
            expect(_.repository.find_by_id(IRRELEVANT_ID)).to.be.equal(_.aggregate)

        def it_returns_none_when_no_aggregate_with_provided_id_is_found():
            with _.storage: _.storage.get_aggregate_changes(IRRELEVANT_ID).returns([])
            expect(_.repository.find_by_id(IRRELEVANT_ID)).to.be.equal(None)
            assert_that(_.aggregate_class.from_events, never(called()))
