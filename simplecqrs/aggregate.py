class Aggregate(object):
    def __init__(self):
        self.uncommitted_changes = []

    @classmethod
    def from_events(cls):
        raise NotImplementedError()

    def changes_committed(self):
        self.uncommitted_changes = []

    def _apply_changes(self, event):
        self.uncommitted_changes.append(event)
        event.apply_changes(self)
