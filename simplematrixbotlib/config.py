from dataclasses import dataclass
import toml

@dataclass
class Config:
    _join_on_invite: bool = True

    def _load_config_dict(self, config_dict: dict) -> None:
        _settings: dict = {
            'join_on_invite': self.set_join_on_invite
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
        