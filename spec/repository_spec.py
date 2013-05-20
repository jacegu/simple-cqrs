from mamba import describe, context, before
from doublex import *

IRRELEVANT_ID = 'irrelevant id'
IRRELEVANT_CHANGE1 = 'irrelevant change 1'
IRRELEVANT_CHANGE2 = 'irrelevant change 2'


with describe(Repository) as _:

    @before.each
    def create_repository():
        _.storage = Spy()
        _.repository = Repository(_.storage)

    with context('saving an aggregate'):
        def it_saves_all_uncommited_changes():
            aggregate = Stub()
            aggregate.id = IRRELEVANT_ID
            aggregate.uncommitted_changes = [IRRELEVANT_CHANGE1, IRRELEVANT_CHANGE2]
            _.repository.save(aggregate)
            assert_that(_.storage.push, called().with_args(IRRELEVANT_ID, IRRELEVANT_CHANGE1))
            assert_that(_.storage.push, called().with_args(IRRELEVANT_ID, IRRELEVANT_CHANGE2))
