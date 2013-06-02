class Repository(object):
    def __init__(self, klass, storage):
        self.klass = klass
        self.storage = storage

    def save(self, aggregate):
        for change in aggregate.uncommitted_changes:
            self.storage.push(aggregate.id, change)
        aggregate.changes_committed()

    def find_by_id(self, id):
        return self._create_aggregate_from_events(self.storage.get_aggregate_changes(id))

    def _create_aggregate_from_events(self, events):
        return None if len(events) is 0 else self.klass.from_events(events)
