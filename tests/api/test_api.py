import pytest
import simplematrixbotlib as botlib


def test_check_valid_homeserver():
    creds = botlib.Creds("https://example.com", "user", "pass")
    bot = botlib.Bot(creds)
    with pytest.raises(ValueError):
        bot.run()

    creds = botlib.Creds("matrix.org", "user", "pass")
    bot = botlib.Bot(creds)
    with pytest.raises(ValueError):
        bot.run()

    creds = botlib.Creds("https://matrix.org", "user", "pass")
    bot = botlib.Bot(creds)
    try:
        bot.run()
    except Exception as e:
        # Trying to catch LoginError normally causes an error - TypeError: catching classes that do not inherit from BaseException is not allowed
        # This is an issue with matrix-nio
        if 'LoginError: M_FORBIDDEN Invalid username or password' in str(e):
            pass
        else:
            raise e

    creds = botlib.Creds("https://example.com", "user", "pass")
    with pytest.raises(ValueError):
        creds.session_write_file()

    # TODO: test loading of broken file?
