from mamba import describe, context, before
from sure import *

with describe('FakeBus') as _:

    with context('registering handlers'):
        def it_registers_the_first_handler_for_a_command_or_event():
            _.bus = FakeBus()
            _.bus.register_handler(IRRELEVANT_EVENT_TYPE, IRRELEVANT_HANDLER)
            expect(_.bus.routes).to.have.key(IRRELEVANT_EVENT_TYPE)
            expect(_.bus.routes.get(IRRELEVANT_EVENT_TYPE)).to.be.equal([IRRELEVANT_HANDLER])

    with context('queueing commands'):
        pass

    with context('publishing events'):
        pass
