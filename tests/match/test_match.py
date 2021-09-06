from simplematrixbotlib.match import Match
from unittest import mock

match = Match(mock.MagicMock(), mock.MagicMock(), mock.MagicMock())

def test_init():
    assert isinstance(match.room, mock.MagicMock)
    assert isinstance(match.event, mock.MagicMock)
    assert isinstance(match._bot, mock.MagicMock)