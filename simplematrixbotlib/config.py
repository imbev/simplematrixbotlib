from dataclasses import dataclass, field
import toml
import re

@dataclass
class Config:
    join_on_invite: bool = True
    allowlist: set[str] = field(default_factory=set)  #TODO: default to bot's homeserver
    blocklist: set[str] = field(default_factory=set)

    def _load_config_dict(self, config_dict: dict) -> None:
        _settings: dict = {
            'join_on_invite': self.set_join_on_invite,
            'allowlist': self.set_allowlist,
            'blocklist': self.set_blocklist
            }
            
        for key, value in config_dict.items():
            if key in _settings.keys():
                _settings[key](value)

    def load_toml(self, file_path: str) -> None:
        with open(file_path, 'r') as file:
            config_dict: dict = toml.load(file)['simplematrixbotlib']['config']
            self._load_config_dict(config_dict)
    
    def set_join_on_invite(self, value: bool) -> None:
        self.join_on_invite = value

    def set_allowlist(self, value: set[str]) -> None:
        self.allowlist = set(map(re.compile, value))

    def add_allowlist(self, value: set[str]) -> None:
        self.allowlist = self.allowlist.union(set(map(re.compile, value)))

    def set_blocklist(self, value: set[str]) -> None:
        self.blocklist = set(map(re.compile, value))

    def add_blocklist(self, value: set[str]) -> None:
        self.blocklist = self.blocklist.union(set(map(re.compile, value)))
