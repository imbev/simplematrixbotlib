from simplematrixbotlib.listener import Listener
from unittest import mock

mock_bot = mock.MagicMock()

listener = Listener(mock_bot)

def test_init():
    assert isinstance(listener._bot, mock.MagicMock)
    assert listener._registry == []
    assert listener._startup_registry == []
