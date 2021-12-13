from simplematrixbotlib.match import Match
from simplematrixbotlib.config import Config
from unittest import mock
import pathlib, os.path

mock_room = mock.MagicMock()

mock_event = mock.MagicMock()
mock_event.sender = "123"

mock_bot = mock.MagicMock()
mock_bot.async_client.user_id = "botid"

match = Match(mock_room, mock_event, mock_bot)

match_config = Match(mock_room, mock_event, mock_bot)
match_config._bot.config = Config()
match_config._bot.config.load_toml(os.path.join(pathlib.Path(__file__).parent.parent, 'config', 'sample_config_files', 'config1.toml'))

def test_init():
    assert isinstance(match.room, mock.MagicMock)
    assert isinstance(match.event, mock.MagicMock)
    assert isinstance(match._bot, mock.MagicMock)

def test_is_from_userid():
    assert match.is_from_userid("123")
    assert not match.is_from_userid("456")

def test_allow_block():
    match_config.event.sender = "@test:example.org"
    assert match_config.is_from_allowed_user()

    match_config.event.sender = "@test2:example.org"
    assert not match_config.is_from_allowed_user()

    match_config.event.sender = "@test:matrix.org"
    assert match_config.is_from_allowed_user()

    match_config.event.sender = "@test2:matrix.org"
    assert not match_config.is_from_allowed_user()

def test_is_not_from_this_bot():
    assert match.is_not_from_this_bot()
