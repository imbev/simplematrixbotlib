from dataclasses import dataclass, field
import toml
import re
from typing import Set


@dataclass
class Config:
    _join_on_invite: bool = True
    _allowlist: Set[re.Pattern] = field(
        default_factory=set)  # TODO: default to bot's homeserver
    _blocklist: Set[re.Pattern] = field(default_factory=set)

    @staticmethod
    def _check_set_regex(value: Set[str]):
        """Checks if the patterns in value are valid or throws an error"""
        for v in value:
            try:
                re.compile(v)   # Fails for invalid regex
            except re.error:
                raise re.error(f"{v} is not a valid regex.")


    def _load_config_dict(self, config_dict: dict) -> None:
        for key, value in config_dict.items():
            if key == 'join_on_invite':
                self.join_on_invite = value
            elif key == 'allowlist':
                self.allowlist = value
            elif key == 'blocklist':
                self.blocklist = value

    def load_toml(self, file_path: str) -> None:
        with open(file_path, 'r') as file:
            config_dict: dict = toml.load(file)['simplematrixbotlib']['config']
            self._load_config_dict(config_dict)

    def save_toml(self, file_path: str) -> None:
        tmp = {
            'simplematrixbotlib': {
                'config': {
                    'join_on_invite': self._join_on_invite,
                    'allowlist': [l.pattern for l in self._allowlist],
                    'blocklist': [l.pattern for l in self._blocklist]
                }
            }
        }
        with open(file_path, 'w') as file:
            toml.dump(tmp, file)

    @property
    def join_on_invite(self) -> bool:
        """
        Returns
        -------
        boolean
            Whether the bot is configured to automatically accept all invites it receives
        """
        return self._join_on_invite

    @join_on_invite.setter
    def join_on_invite(self, value: bool) -> None:
        self._join_on_invite = value

    @property
    def allowlist(self) -> Set[re.Pattern]:
        """
        Returns
        -------
        Set[re.Pattern]
            A set of regular expressions matching Matrix IDs.
            Can be used in conjunction with blocklist to check if the sender is allowed to issue a command to the bot.
            An empty set implies that everyone is allowed.
        """
        return self._allowlist

    @allowlist.setter
    def     allowlist(self, value: Set[str]) -> None:
        self._check_set_regex(value)
        self._allowlist = value

    def add_allowlist(self, value: Set[str]):
        """
        Adds all regex to the allowlist if valid, else throws error

        Parameters
        ----------
        value : Set[str]
            A set of strings which represent Matrix IDs or a regular expression matching Matrix IDs to be added to allowlist.
        """
        self._check_set_regex(value)
        self._allowlist = self._allowlist.union(value)

    def remove_allowlist(self, value: Set[str]):
        """
        Removes all in the value set from the allowlist or throws an error

        Parameters
        ----------
        value : Set[str]
            A set of strings which represent Matrix IDs or a regular expression matching Matrix IDs to be removed from allowlist.
        """
        self._check_set_regex(value)
        self._allowlist = self._allowlist - value

    @property
    def blocklist(self) -> Set[re.Pattern]:
        """
        Returns
        -------
        Set[re.Pattern]
            A set of regular expressions matching Matrix IDs.
            Can be used in conjunction with allowlist to check if the sender is disallowed to issue a command to the bot.
        """
        return self._blocklist

    @blocklist.setter
    def blocklist(self, value: Set[str]) -> None:
        self._check_set_regex(value)
        self._blocklist = value

    def add_blocklist(self, value: Set[str]) -> None:
        """
        Parameters
        ----------
        value : Set[str]
            A set of strings which represent Matrix IDs or a regular expression matching Matrix IDs to be added to blocklist.
        """
        self._check_set_regex(value)
        self._blocklist = self._blocklist.union(value)

    def remove_blocklist(self, value: Set[str]) -> None:
        """
        Parameters
        ----------
        value : Set[str]
            A set of strings which represent Matrix IDs or a regular expression matching Matrix IDs to be removed from blocklist.
        """
        self._check_set_regex(value)
        self._blocklist = self._blocklist - value
