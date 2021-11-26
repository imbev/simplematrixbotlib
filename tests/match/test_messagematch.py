from simplematrixbotlib.match import MessageMatch, Match
from unittest import mock

mock_room = mock.MagicMock()

mock_room2 = mock.MagicMock()
mock_room2.own_user_id = "@bot:matrix.org"
mock_user = mock.MagicMock()
mock_user.display_name = "bot"
mock_user.disambiguated_name = f"{mock_user.display_name} ({mock_room2.own_user_id})"
mock_room2.users = {mock_room2.own_user_id: mock_user}

mock_event = mock.MagicMock()
mock_event.body = "p!help example"

mock_event2 = mock.MagicMock()
mock_event2.body = "p!help"

mock_event3 = mock.MagicMock()
mock_event3.body = "bot help"
mock_event3.formatted_body = None
mock_event4 = mock.MagicMock()
mock_event4.body = "bot: help"
mock_event4.formatted_body = None
mock_event5 = mock.MagicMock()
mock_event5.body = f"{mock_room2.own_user_id} help"
mock_event5.formatted_body = None
mock_event6 = mock.MagicMock()
mock_event6.body = f"bot ({mock_room2.own_user_id}) help"
mock_event6.formatted_body = None
mock_event7 = mock.MagicMock()
mock_event7.body = "something else"
mock_event7.formatted_body = "<a href=\"https://matrix.to/#/@bot:matrix.org\">bot</a> help"
mock_event8 = mock.MagicMock()
mock_event8.body = "bottom help"
mock_event8.formatted_body = None

mock_bot = mock.MagicMock()

prefix = "p!"
prefix2 = "!!"

match = MessageMatch(mock_room, mock_event, mock_bot, prefix)      # prefix match
match2 = MessageMatch(mock_room, mock_event, mock_bot)             # no prefix given
match3 = MessageMatch(mock_room, mock_event, mock_bot, prefix2)    # wrong prefix given
match4 = MessageMatch(mock_room, mock_event2, mock_bot, prefix)    # no arguments given

match5 = MessageMatch(mock_room2, mock_event3, mock_bot, prefix)   # mention with display name
match6 = MessageMatch(mock_room2, mock_event4, mock_bot, prefix)   # mention with colon
match7 = MessageMatch(mock_room2, mock_event5, mock_bot, prefix)   # mention with user id
match8 = MessageMatch(mock_room2, mock_event6, mock_bot, prefix)   # mention with disambiguated name
match9 = MessageMatch(mock_room2, mock_event7, mock_bot, prefix)   # mention with pill
match10 = MessageMatch(mock_room2, mock_event8, mock_bot, prefix)  # mention someone else

def test_init():
    assert issubclass(MessageMatch, Match)
    assert match._prefix == prefix

def test_command():
    assert match.command() == "help"
    assert match.command("help") == True

    assert match2.command() == "p!help"
    assert match2.command("p!help") == True

def test_mention():
    assert match5.command() == "help"
    assert match5.mention() == True

    assert match6.command() == "help"
    assert match6.mention() == True

    assert match7.command() == "help"
    assert match7.mention() == True

    assert match8.command() == "help"
    assert match8.mention() == True

    assert match9.command() == "help"
    assert match9.mention() == True

    assert match10.command() == "bottom"
    assert match10.mention() == False

def test_prefix():
    assert match.prefix() == True
    assert match3.prefix() == False

    #assert match2.prefix() == True

def test_args():
    assert match.args() == ["example"]

    assert match4.args() == []

def test_contains():
    assert match.contains("!h") == True
    assert match.contains("lp exam") == True
    assert match.contains("nothing") == False

match = MessageMatch(mock_room, mock_event, mock_bot, prefix)

def test_init():
    assert issubclass(MessageMatch, Match)
    assert match._prefix == prefix
