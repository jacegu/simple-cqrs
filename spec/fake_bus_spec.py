from mamba import describe, context, before, skip
from sure import *
from doublex import *


from spec.constants import *


class FakeBus(object):
    def __init__(self):
        self.routes = {}

    def register_handler(self, event_or_command, handler):
        self.routes.setdefault(event_or_command, []).append(handler)

    def send(self, command):
        self._handler_for(command).handle(command)

    def _handler_for(self, command):
        return self.routes[type(command)][0]


class DummyCommand(object):
    pass

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

    with context('sending commands'):
        def it_handles_the_event_if_the_command_has_a_single_handler():
            handler = Spy()
            command = DummyCommand()
            _.bus.register_handler(DummyCommand, handler)
            _.bus.send(command)
            assert_that(handler.handle, called().with_args(command))

        def it_raises_an_error_if_the_command_has_more_than_one_handler():
            command = DummyCommand()
            _.bus.register_handler(DummyCommand, IRRELEVANT_HANDLER1)
            _.bus.register_handler(DummyCommand, IRRELEVANT_HANDLER2)
            expect(_.bus.send).when.called_with(command).to.throw(InvalidOperationError)

        @skip
        def it_raises_an_error_if_no_handler_for_command_is_found():
            pass

    with context('publishing events'):
        pass
