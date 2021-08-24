from nio import RoomMessageText


class Listener:
    def __init__(self, bot):
        self._bot = bot
        self._registry = []
        self._startup_registry = []

    def on_custom_event(self, event):
        def wrapper(func):
            if [func, event] in self._registry:
                func()
            else:
                self._registry.append([func, event])

        return wrapper

    def on_message_event(self, func):
        if [func, RoomMessageText] in self._registry:
            func()
        else:
            self._registry.append([func, RoomMessageText])

    def on_startup(self, func):
        if func in self._startup_registry:
            func()
        else:
            self._startup_registry.append(func)
