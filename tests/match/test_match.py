from simplematrixbotlib.match import Match
from unittest import mock

mock_room = mock.MagicMock()
mock_event = mock.MagicMock()
mock_bot = mock.MagicMock()
match = Match(mock_room, mock_event, mock_bot)

def test_init():
    assert isinstance(match.room, mock.MagicMock)
    assert isinstance(match.event, mock.MagicMock)
    assert isinstance(match._bot, mock.MagicMock)

def test_is_from_userid():
    mock_event.sender = "123"
    assert match.is_from_userid("123")
    assert not match.is_from_userid("456")