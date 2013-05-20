from mamba import describe, context, before
from doublex import *

IRRELEVANT_ID = 'irrelevant id'
IRRELEVANT_CHANGE1 = 'irrelevant change 1'
IRRELEVANT_CHANGE2 = 'irrelevant change 2'

class Repository(object):
    def __init__(self, storage):
        self.storage = storage

    def save(self, aggregate):
        for change in aggregate.uncommitted_changes:
            self.storage.push(aggregate.id, change)
        aggregate.changes_committed()


with describe(Repository) as _:

    @before.each
    def create_repository():
        _.storage = Spy()
        _.repository = Repository(_.storage)

    @before.each
    def create_aggregate():
        _.aggregate = Spy()
        _.aggregate.id = IRRELEVANT_ID
        _.aggregate.uncommitted_changes = [IRRELEVANT_CHANGE1, IRRELEVANT_CHANGE2]

    with context('saving an aggregate'):
        def it_saves_all_uncommited_changes():
            _.repository.save(_.aggregate)
            assert_that(_.storage.push, called().with_args(IRRELEVANT_ID, IRRELEVANT_CHANGE1))
            assert_that(_.storage.push, called().with_args(IRRELEVANT_ID, IRRELEVANT_CHANGE2))

        def it_marks_the_changes_as_committed():
            _.repository.save(_.aggregate)
            assert_that(_.aggregate.changes_committed, called())

