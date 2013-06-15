from mamba import describe, context, before, skip
from sure import *
from doublex import *

from spec.constants import *

from simplecqrs.fake_bus import FakeBus
from simplecqrs.errors import InvalidOperationError


class DummyCommand(object):
    pass

class DummyEvent(object):
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
        @before.each
        def create_command():
            _.command = DummyCommand()

        def it_handles_the_event_if_the_command_has_a_single_handler():
            handler = Spy()
            _.bus.register_handler(DummyCommand, handler)
            _.bus.send(_.command)
            assert_that(handler.handle, called().with_args(_.command))

        def it_raises_an_error_if_the_command_has_more_than_one_handler():
            _.bus.register_handler(DummyCommand, IRRELEVANT_HANDLER1)
            _.bus.register_handler(DummyCommand, IRRELEVANT_HANDLER2)
            expect(_.bus.send).when.called_with(_.command).to.throw(InvalidOperationError)

        def it_raises_an_error_if_no_handler_for_command_is_found():
            expect(_.bus.send).when.called_with(_.command).to.throw(InvalidOperationError)

    with context('publishing events'):
        @before.each
        def create_event():
            _.event = DummyEvent()
            _.handler = Spy()

        def it_dispatches_the_handler_for_the_published_event():
            _.bus.register_handler(DummyEvent, _.handler)
            _.bus.publish(_.event)
            assert_that(_.handler.handle, called().with_args(_.event))

        def it_does_nothing_when_no_halder_for_published_event_is_found():
            _.bus.publish(_.event)
            assert_that(_.handler.handle, never(called()))

