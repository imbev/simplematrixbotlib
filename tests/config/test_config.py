import pytest
import pathlib
import pytest
import simplematrixbotlib as botlib
import os.path
import re
from dataclasses import dataclass

sample_config_path = os.path.join(
    pathlib.Path(__file__).parent, 'sample_config_files')

@dataclass
class SimpleConfig(botlib.Config):
    simple_setting: str = "Default"

@dataclass
class UpperConfig(botlib.Config):
    _simple_setting: str = "Default"

    @property
    def simple_setting(self) -> str:
        return self._simple_setting

    @simple_setting.setter
    def simple_setting(self, value: str) -> None:
        self._simple_setting = value.upper()


def test_defaults():
    config = botlib.Config()

    assert config.join_on_invite
    assert config.allowlist == set()
    assert config.blocklist == set()

    config = SimpleConfig()
    assert config.simple_setting == "Default"

    config = UpperConfig()
    assert config.simple_setting == "Default"


def test_read_toml():
    config = botlib.Config()
    # load non-defaults
    config.load_toml(os.path.join(sample_config_path, 'config1.toml'))
    assert not config.join_on_invite
    assert set(config.allowlist) == set(
        map(re.compile, ['.*:example\\.org', '@test:matrix\\.org']))
    assert set(config.blocklist) == set(
        map(re.compile, ['@test2:example\\.org']))

    config = botlib.Config()
    # load defaults
    config.load_toml(os.path.join(sample_config_path, 'config2.toml'))
    assert config.join_on_invite

    config = botlib.Config()
    # load defaults from an empty config
    config.load_toml(os.path.join(sample_config_path, 'config3.toml'))
    assert config.join_on_invite

    config = botlib.Config()
    # config4.toml uses invalid regular expression syntax
    config.load_toml(os.path.join(sample_config_path, 'config4.toml'))
    assert config.blocklist == set()

    config = botlib.Config()
    # config5.toml contains an unsupported field called "custom"
    config.load_toml(os.path.join(sample_config_path, 'config5.toml'))
    with pytest.raises(AttributeError):
        assert config.custom is None

    config = SimpleConfig()
    # config6.toml contains a custom 'simple_setting' string
    config.load_toml(os.path.join(sample_config_path, 'config6.toml'))
    assert config.simple_setting == "Hello World"

    config = UpperConfig()
    # config6.toml contains a custom 'simple_setting' string
    config.load_toml(os.path.join(sample_config_path, 'config6.toml'))
    assert config.simple_setting == "HELLO WORLD"


def test_write_toml():
    tmp_file = os.path.join(sample_config_path, 'config_tmp.toml')
    config = botlib.Config()
    # write all defined values
    config.save_toml(tmp_file)

    default_values = ("[simplematrixbotlib.config]\n"
                      "join_on_invite = true\n"
                      "allowlist = []\n"
                      "blocklist = []\n"
                     )
    assert os.path.isfile(tmp_file)
    with open(tmp_file, 'r') as f:
        assert f.read() == default_values

    config.custom = "custom value"
    # don't write custom values
    config.save_toml(tmp_file)
    with open(tmp_file, 'r') as f:
        assert f.read() == default_values

    config = SimpleConfig()
    # write a custom value correctly (underscore etc)
    config.save_toml(tmp_file)
    with open(tmp_file, 'r') as f:
        assert "simple_setting = \"Default\"\n" in f.readlines()

    config = UpperConfig()
    # write a custom value correctly
    config.save_toml(tmp_file)
    with open(tmp_file, 'r') as f:
        assert "simple_setting = \"Default\"\n" in f.readlines()


def test_manual_set():
    config = botlib.Config()
    config.join_on_invite = True
    assert config.join_on_invite

    config.join_on_invite = False
    assert not config.join_on_invite

    config = botlib.Config()
    config.allowlist = {'.*:example\\.org'}
    assert re.compile('.*:example\\.org') in config.allowlist
    config.add_allowlist({'@test:matrix\\.org'})
    assert config.allowlist == set(
        map(re.compile, ['.*:example\\.org', '@test:matrix\\.org']))
    config.remove_allowlist({'.*:example\\.org'})
    assert config.allowlist == set(map(re.compile, ['@test:matrix\\.org']))
    config.allowlist = {'*:example\\.org'}
    assert config.allowlist == set(map(re.compile, ['@test:matrix\\.org']))

    config.blocklist = {'.*:example\\.org'}
    assert re.compile('.*:example\\.org') in config.blocklist
    config.add_blocklist({'@test:matrix\\.org'})
    assert config.blocklist == set(
        map(re.compile, ['.*:example\\.org', '@test:matrix\\.org']))
    config.remove_blocklist({'.*:example\\.org'})
    assert config.blocklist == set(map(re.compile, ['@test:matrix\\.org']))
    config.blocklist = {'*:example\\.org'}
    assert config.blocklist == set(map(re.compile, ['@test:matrix\\.org']))

    config = UpperConfig()
    config.simple_setting = "test"
    assert config.simple_setting == "TEST"
