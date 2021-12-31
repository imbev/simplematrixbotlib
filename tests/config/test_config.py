import pathlib
import pytest
import simplematrixbotlib as botlib
import os.path
import re

sample_config_path = os.path.join(
    pathlib.Path(__file__).parent, 'sample_config_files')


def test_defaults():
    config = botlib.Config()

    assert config.join_on_invite
    assert config.allowlist == set()
    assert config.blocklist == set()


def test_read_toml():
    config = botlib.Config()
    config.load_toml(os.path.join(sample_config_path, 'config1.toml'))
    assert not config.join_on_invite
    assert set(config.allowlist) == set(
        map(re.compile, ['.*:example\\.org', '@test:matrix\\.org']))
    assert set(config.blocklist) == set(
        map(re.compile, ['@test2:example\\.org']))

    config = botlib.Config()
    config.load_toml(os.path.join(sample_config_path, 'config2.toml'))
    assert config.join_on_invite

    config = botlib.Config()
    config.load_toml(os.path.join(sample_config_path, 'config3.toml'))
    assert config.join_on_invite

    config = botlib.Config()
    # config4.toml uses invalid regular expression syntax
    config.load_toml(os.path.join(sample_config_path, 'config4.toml'))
    assert config.blocklist == set()

    # TODO: test botlib.Bot() constructor creating a default Config


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
