from nio import RoomMessageText, UnknownEvent


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

    def on_reaction_event(self, func):

        async def new_func(room, event):
            if event.type == "m.reaction":
                await func(room, event,
                           event.source['content']['m.relates_to']['key'])

        self._registry.append([new_func, UnknownEvent])

    def on_startup(self, func):
        if func in self._startup_registry:
            func()
        else:
            self._startup_registry.append(func)
