from typing import List
from simplematrixbotlib.listener import Listener
from unittest import mock
from nio import RoomMessageText

mock_bot = mock.MagicMock()

mock_event = mock.MagicMock()

listener = Listener(mock_bot)

def test_init():
    assert isinstance(listener._bot, mock.MagicMock)
    assert listener._registry == []
    assert listener._startup_registry == []

def test_on_custom_event():
    @listener.on_custom_event(mock_event)
    def example():
        return "example"
    
    def check():
        for func_event in listener._registry:
            if func_event[0]() == "example" and func_event[1] == mock_event:
                return True
        return False
    
    assert check() == True

def test_on_message_event():
    @listener.on_message_event
    def example2():
        return "example2"
    
    def check():
        for func_event in listener._registry:
            if func_event[0]() == "example2" and func_event[1] == RoomMessageText:
                return True
        return False
    
    assert check() == True

def test_on_startup():
    @listener.on_startup
    def example3():
        return "example3"
    
    def check():
        for func in listener._startup_registry:
            if func() == "example3":
                return True
        return False

    assert check()