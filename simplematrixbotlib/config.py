from dataclasses import dataclass, field
import toml

@dataclass
class Config:
    _join_on_invite: bool = True
    allowlist: list[str] = field(default_factory=list)  #TODO: default to bot's homeserver
    blocklist: list[str] = field(default_factory=list)

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
            toml_content: str = file.read()
            config_dict: dict = toml.loads(toml_content)['simplematrixbotlib']['config']
            self._load_config_dict(config_dict)
    
    def set_join_on_invite(self, value: bool) -> None:
        self._join_on_invite = value

    def set_allowlist(self, value: list) -> None:
        self.allowlist = value

    def add_allowlist(self, value: list) -> None:
        self.allowlist = list(set(self.allowlist + value))

    def set_blocklist(self, value: list) -> None:
        self.blocklist = value

    def add_blocklist(self, value: list) -> None:
        self.blocklist = list(set(self.blocklist + value))
