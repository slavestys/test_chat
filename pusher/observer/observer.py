from collections import defaultdict


class Observer:
    def __init__(self):
        self.event_handlers = defaultdict(list)

    def register(self, event, handler):
        self.event_handlers[event].append(handler)

    def emit(self, event, *args, **kwargs):
        for handler in self.event_handlers[event]:
            handler(*args, **kwargs)
