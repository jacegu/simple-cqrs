from simplecqrs.errors import InvalidOperationError

class FakeBus(object):
    def __init__(self):
        self.routes = {}

    def register_handler(self, event_or_command, handler):
        self.routes.setdefault(event_or_command, []).append(handler)

    def send(self, command):
        self._handler_for(command).handle(command)

    def publish(self, event):
        for handler in self._all_handlers_for(event):
            handler.handle(event)
            return

    def _handler_for(self, command):
        self._check_that_has_handlers(command)
        self._check_that_has_a_single_handler(command)
        return self._all_handlers_for(command)[0]

    def _check_that_has_handlers(self, command):
        if not type(command) in self.routes:
            raise(InvalidOperationError('No handler for command ' + str(type(command)) + ' found'))

    def _check_that_has_a_single_handler(self, command):
        if len(self._all_handlers_for(command)) > 1:
            raise(InvalidOperationError(str(type(command)) + ' has more than one handler'))

    def _all_handlers_for(self, event_or_command):
        return self.routes.get(type(event_or_command), [])
