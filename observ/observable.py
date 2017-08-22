class ObservableMixin:
    def __init__(self):
        self._subscribers = []

    def subscribe(self, subscriber):
        self._subscribers.append(subscriber)

    def is_subscribed(self, subscriber):
        return subscriber in self._subscribers

    def unsubscribe(self, subscriber):
        self._subscribers.remove(subscriber)

    def notify(self, *args, **kwargs):
        for subscriber in self._subscribers:
            subscriber(*args, **kwargs)
