from simplecqrs.errors import InvalidOperationError

class FakeBus(object):
    def __init__(self):
        self.routes = {}

    def register_handler(self, event_or_command, handler):
        self.routes.setdefault(event_or_command, []).append(handler)

    def send(self, command):
        self._handler_for(command).handle(command)

    def publish(self, event):
        self._handler_for(event).handle(event)

    def _handler_for(self, event_or_command):
        self._check_that_has_handlers(event_or_command)
        self._check_that_has_a_single_handler(event_or_command)
        return self._all_handers_for(event_or_command)[0]

    def _check_that_has_handlers(self, event_or_command):
        if not type(event_or_command) in self.routes:
            raise(InvalidOperationError('No handler for event_or_command ' + str(type(event_or_command)) + ' found'))

    def _check_that_has_a_single_handler(self, event_or_command):
        if len(self._all_handers_for(event_or_command)) > 1:
            raise(InvalidOperationError(str(type(event_or_command)) + ' has more than one handler'))

    def _all_handers_for(self, event_or_command):
        return self.routes[type(event_or_command)]
