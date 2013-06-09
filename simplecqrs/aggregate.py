class Aggregate(object):
    def __init__(self):
        self.uncommitted_changes = []

    @classmethod
    def from_events(cls, events):
        aggregate = cls()
        for event in events: event.apply_changes(aggregate, False)
        aggregate.uncommitted_changes = []
        return aggregate

    def changes_committed(self):
        self.uncommitted_changes = []

    def _apply_changes(self, event, is_new = True):
        if is_new is True:
            self.uncommitted_changes.append(event)
        event.apply_changes(self)
