from simplematrixbotlib.match import Match
from unittest import mock

mock_room = mock.MagicMock()

mock_event = mock.MagicMock()
mock_event.sender = "123"

mock_bot = mock.MagicMock()
mock_bot.async_client.user_id = "botid"

match = Match(mock_room, mock_event, mock_bot)

def test_init():
    assert isinstance(match.room, mock.MagicMock)
    assert isinstance(match.event, mock.MagicMock)
    assert isinstance(match._bot, mock.MagicMock)

def test_is_from_userid():
    assert match.is_from_userid("123")
    assert not match.is_from_userid("456")

def test_is_not_from_this_bot():
    assert match.is_not_from_this_bot()

def intentional_fail_REMOVE(): ##REMOVE
    assert True == False