import pathlib
import simplematrixbotlib as botlib


sample_config_path = f'{pathlib.Path(__file__).parent}/sample_config_files'

def test_defaults():
    config = botlib.Config()

    assert config._join_on_invite

def test_read_toml():
    config = botlib.Config()
    config.load_toml(f'{sample_config_path}/config1.toml')
    assert not config._join_on_invite
        
    config = botlib.Config()
    config.load_toml(f'{sample_config_path}/config2.toml')
    assert config._join_on_invite

    config = botlib.Config()
    config.load_toml(f'{sample_config_path}/config3.toml')
    assert config._join_on_invite

def test_manual_set():
    config = botlib.Config()
    config.set_join_on_invite(True)
    assert config._join_on_invite

    config.set_join_on_invite(False)
    assert not config._join_on_invite