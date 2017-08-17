class Observable:
    def __init__(self):
        self._subscribers = []
        
    def subscribe(self, subscriber):
        self._subscribers.append(subscriber)
        
    def unsubscribe(self, subscriber):
        self._subscribers.remove(subscriber)
        
    def notify(self, **kwargs):
        for subscriber in self._subscribers:
            subscriber(**kwargs)
