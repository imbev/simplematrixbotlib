import pathlib
import simplematrixbotlib as botlib
import os.path

sample_config_path = os.path.join(pathlib.Path(__file__).parent, 'sample_config_files')

def test_defaults():
    config = botlib.Config()

    assert config.join_on_invite
    assert config.allowlist == list()
    assert config.blocklist == list()

def test_read_toml():
    config = botlib.Config()
    config.load_toml(os.path.join(sample_config_path, 'config1.toml'))
    assert not config.join_on_invite
    assert config.allowlist == ['*:example.org', '@test:matrix.org']
    assert config.blocklist == ['@test2:example.org']
        
    config = botlib.Config()
    config.load_toml(os.path.join(sample_config_path, 'config2.toml'))
    assert config.join_on_invite

    config = botlib.Config()
    config.load_toml(os.path.join(sample_config_path, 'config3.toml'))
    assert config.join_on_invite

def test_manual_set():
    config = botlib.Config()
    config.set_join_on_invite(True)
    assert config.join_on_invite

    config.set_join_on_invite(False)
    assert not config.join_on_invite
