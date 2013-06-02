from mamba import describe, before, context
from sure import expect

from simplecqrs.aggregate import Aggregate


with describe('an example Aggregate') as _:

    def it_starts_with_no_uncommitted_changes():
        _.aggregate = DummyAggregate()
        expect(_.aggregate.uncommitted_changes).to.be.empty
