class Aggregate(object):
    def __init__(self):
        self.uncommitted_changes = []

    @classmethod
    def from_events(cls):
        raise NotImplementedError()

    def changes_committed(self):
        raise NotImplementedError()

