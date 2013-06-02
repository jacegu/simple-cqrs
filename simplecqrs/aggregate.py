class Aggregate(object):
    def __init__(self):
        self.uncommitted_changes = []

    @classmethod
    def from_events(cls):
        raise NotImplementedError()

    def changes_committed(self):
        raise NotImplementedError()

    def _applyChanges(self, event):
        self.uncommitted_changes.append(event)
        event.apply_changes(self)
