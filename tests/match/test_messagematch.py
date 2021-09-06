from simplematrixbotlib.match import MessageMatch, Match
from unittest import mock

mock_room = mock.MagicMock()

mock_event = mock.MagicMock()

mock_bot = mock.MagicMock()

prefix = "p!"

match = MessageMatch(mock_room, mock_event, mock_bot, prefix)

def test_init():
    assert issubclass(MessageMatch, Match)
    assert match._prefix == prefix