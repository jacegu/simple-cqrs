class Aggregate(object):

    @classmethod
    def from_events(cls):
        raise NotImplementedError()

    def changes_committed(self):
        raise NotImplementedError()
