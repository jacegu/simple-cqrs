
class Repository(object):
    FIRST_VERSION = -1

    def __init__(self, klass, storage):
        self.klass = klass
        self.storage = storage

    def save(self, aggregate, version = FIRST_VERSION):
        for change in aggregate.uncommitted_changes:
            self.storage.push(aggregate.id, change, version)
            version += 1
        aggregate.changes_committed()

    def find_by_id(self, id):
        return self._create_aggregate_from_events(self.storage.get_events_for_aggregate(id))

    def _create_aggregate_from_events(self, events):
        return None if len(events) is 0 else self.klass.from_events(events)


class InMemoryEventStore(object):
    def __init__(self, publisher):
        self.publisher = publisher
        self.events = {}

    def push(self, aggregate_id, event, version):
        if self._there_are_events_for(aggregate_id):
            self._verify_version(aggregate_id, version)
        self._store(aggregate_id, event, version)
        self.publisher.publish(event)

    def get_events_for_aggregate(self, aggregate_id):
        if self._there_are_events_for(aggregate_id):
            return [event_data['event'] for event_data in self.events[aggregate_id]]
        else:
            raise AggregateNotFoundError()

    def _there_are_events_for(self, aggregate_id):
        return aggregate_id in self.events

    def _verify_version(self, aggregate_id, provided_version):
        print provided_version
        print self._next_version_of(aggregate_id)
        if provided_version != self._next_version_of(aggregate_id):
            raise ConcurrencyError()

    def _next_version_of(self, aggregate_id):
        return self.events.get(aggregate_id)[-1].get('version') + 1

    def _store(self, aggregate_id, event, version):
        print version
        self.events.setdefault(aggregate_id, []).append({'event': event, 'version': version})


class AggregateNotFoundError(RuntimeError):
    pass

class ConcurrencyError(RuntimeError):
    pass
