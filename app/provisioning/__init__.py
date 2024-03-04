from app.models.netbox import Event


class BaseProvisioning:
    def __init__(self, event: Event):
        self._event = event

        # make a few short-cuts/helpers
        self._pre_change = event.snapshots.pre_change
        self._post_change = event.snapshots.post_change

    def process(self):
        raise NotImplementedError
