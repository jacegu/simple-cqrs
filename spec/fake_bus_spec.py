from mamba import describe, context, before
from sure import *


from spec.constants import *


class FakeBus(object):
    def __init__(self):
        self.routes = {}

    def register_handler(self, message, handler):
        if not message in self.routes:
            self.routes[message] = []
        self.routes[message].append(handler)



with describe('FakeBus') as _:

    @before.each
    def create_fake_bus():
        _.bus = FakeBus()

    with context('registering handlers'):
        def it_registers_the_first_handler_for_a_command_or_event():
            _.bus.register_handler(IRRELEVANT_EVENT_TYPE, IRRELEVANT_HANDLER1)
            expect(_.bus.routes).to.have.key(IRRELEVANT_EVENT_TYPE)
            expect(_.bus.routes.get(IRRELEVANT_EVENT_TYPE)).to.be.equal([IRRELEVANT_HANDLER1])

        def it_registers_more_than_one_handler_per_command_or_event():
            _.bus.register_handler(IRRELEVANT_EVENT_TYPE, IRRELEVANT_HANDLER1)
            _.bus.register_handler(IRRELEVANT_EVENT_TYPE, IRRELEVANT_HANDLER2)
            expect(_.bus.routes).to.have.key(IRRELEVANT_EVENT_TYPE)
            expect(_.bus.routes.get(IRRELEVANT_EVENT_TYPE)).to.be.equal([IRRELEVANT_HANDLER1, IRRELEVANT_HANDLER2])

    with context('queueing commands'):
        pass

    with context('publishing events'):
        pass
