import pathlib
import simplematrixbotlib as botlib
import os.path

sample_config_path = os.path.join(pathlib.Path(__file__).parent, 'sample_config_files')

def test_defaults():
    config = botlib.Config()

    assert config._join_on_invite
    assert config.allowlist == list()
    assert config.blocklist == list()

def test_read_toml():
    config = botlib.Config()
    assert not config._join_on_invite
    config.load_toml(os.path.join(sample_config_path, 'config1.toml'))
    assert config.allowlist == ['*:example.org', '@test:matrix.org']
    assert config.blocklist == ['@test2:example.org']
        
    config = botlib.Config()
    assert config._join_on_invite
    config.load_toml(os.path.join(sample_config_path, 'config2.toml'))

    config = botlib.Config()
    assert config._join_on_invite
    config.load_toml(os.path.join(sample_config_path, 'config3.toml'))

def test_manual_set():
    config = botlib.Config()
    config.set_join_on_invite(True)
    assert config._join_on_invite

    config.set_join_on_invite(False)
    assert not config._join_on_invite