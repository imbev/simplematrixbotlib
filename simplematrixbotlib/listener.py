from nio import RoomMessageText

class Listener:
    def __init__(self, bot):
        self._bot = bot
        self._registry = []
    
    def _make_dec_with_arg(self, decorator):
        def layer(*args, **kwargs):
            def repl(function):
                return decorator(function, *args, **kwargs)
            return repl
        return layer
    
    @self._make_dec_with_arg
    def custom_event(self, handler, event_type: str):
        self._registry.append([event_type, handler])
    
    @self._make_dec_with_arg
    def message_event(self, handler):
        self._registry.append([RoomMessageText, handler])
