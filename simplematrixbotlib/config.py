from dataclasses import dataclass, field, fields, asdict
import os.path
import toml
import re
from typing import Set, Union
from nio.crypto import ENCRYPTION_ENABLED


def _config_dict_factory(tmp) -> dict:
    return {
        'simplematrixbotlib': {
            'config':
            {_strip_leading_underscore(name): value
             for name, value in tmp}
        }
    }


def _strip_leading_underscore(tmp: str) -> str:
    return tmp[1:] if tmp[0] == '_' else tmp


def _check_set_regex(value: Set[str]) -> Union[Set[re.Pattern], None]:
    new_list = set()
    for v in value:
        try:
            tmp = re.compile(v)
        except re.error:
            print(
                f"{v} is not a valid regular expression. Ignoring your list update."
            )
            return None
        new_list.add(tmp)
    return new_list


@dataclass
class Config:
    """
    A class to handle built-in user-configurable settings, including support for saving to and loading from a file.
    Can be inherited from by bot developers to implement custom settings.
    """

    _join_on_invite: bool = True
    _encryption_enabled: bool = ENCRYPTION_ENABLED
    _emoji_verify: bool = False  # So users who enable it are aware of required interactivity
    _ignore_unverified_devices: bool = True  # True by default in Element
    # TODO: auto-ignore/auto-blacklist devices/users
    # _allowed_unverified_devices etc
    _store_path: str = "./store/"
    _allowlist: Set[re.Pattern] = field(
        default_factory=set)  # TODO: default to bot's homeserver
    _blocklist: Set[re.Pattern] = field(default_factory=set)

    def _load_config_dict(self, config_dict: dict) -> None:
        # TODO: make this into a factory, so defaults for
        # non-loaded values can be set based on loaded values?
        existing_fields = [
            _strip_leading_underscore(f.name) for f in fields(self)
        ]
        for key, value in config_dict.items():
            if key not in existing_fields:
                continue
            setattr(self, key, value)

    def load_toml(self, file_path: str) -> None:
        with open(file_path, 'r') as file:
            config_dict: dict = toml.load(file)['simplematrixbotlib']['config']
            self._load_config_dict(config_dict)

    def save_toml(self, file_path: str) -> None:
        tmp = asdict(self, dict_factory=_config_dict_factory)
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
    def encryption_enabled(self) -> bool:
        """
        Returns
        -------
        boolean
            Whether to enable encryption support.
            Requires encryption-specific dependencies to be met, see install instructions.
        """
        return self._encryption_enabled

    @encryption_enabled.setter
    def encryption_enabled(self, value: bool) -> None:
        # safeguards regarding ENCRYPTION_ENABLED are enforced by nio in ClientConfig
        self._encryption_enabled = value
        # update dependent values
        self.emoji_verify = self.emoji_verify
        self.ignore_unverified_devices = self.ignore_unverified_devices

    @property
    def emoji_verify(self) -> bool:
        """
        Returns
        -------
        boolean
            Whether emoji verification requests should be handled by the built in callback function
        """
        return self._emoji_verify

    @emoji_verify.setter
    def emoji_verify(self, value: bool) -> None:
        self._emoji_verify = value and self.encryption_enabled

    @property
    def store_path(self) -> str:
        """
        Returns
        -------
        string
            Where to store crypto-related data including keys
        """
        return self._store_path

    @store_path.setter
    def store_path(self, value: str) -> None:
        # check if the path exists or can be created, throws an error otherwise
        os.makedirs(value, mode=0o750, exist_ok=True)
        self._store_path = value

    @property
    def ignore_unverified_devices(self) -> bool:
        """
        Returns
        -------
        boolean
            If True, ignore that devices are not verified and send the message to them regardless.
            If False, distrust unverified devices.
        """
        return self._ignore_unverified_devices

    @ignore_unverified_devices.setter
    def ignore_unverified_devices(self, value: bool) -> None:
        self._ignore_unverified_devices = value if self.encryption_enabled else True

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
    def allowlist(self, value: Set[str]) -> None:
        checked = _check_set_regex(value)
        if checked is None:
            return
        self._allowlist = checked

    def add_allowlist(self, value: Set[str]) -> None:
        """
        Parameters
        ----------
        value : Set[str]
            A set of strings which represent Matrix IDs or a regular expression matching Matrix IDs to be added to allowlist.
        """
        checked = _check_set_regex(value)
        if checked is None:
            return
        self._allowlist = self._allowlist.union(checked)

    def remove_allowlist(self, value: Set[str]) -> None:
        """
        Parameters
        ----------
        value : Set[str]
            A set of strings which represent Matrix IDs or a regular expression matching Matrix IDs to be removed from allowlist.
        """
        checked = _check_set_regex(value)
        if checked is None:
            return
        self._allowlist = self._allowlist - checked

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
        checked = _check_set_regex(value)
        if checked is None:
            return
        self._blocklist = checked

    def add_blocklist(self, value: Set[str]) -> None:
        """
        Parameters
        ----------
        value : Set[str]
            A set of strings which represent Matrix IDs or a regular expression matching Matrix IDs to be added to blocklist.
        """
        checked = _check_set_regex(value)
        if checked is None:
            return
        self._blocklist = self._blocklist.union(checked)

    def remove_blocklist(self, value: Set[str]) -> None:
        """
        Parameters
        ----------
        value : Set[str]
            A set of strings which represent Matrix IDs or a regular expression matching Matrix IDs to be removed from blocklist.
        """
        checked = _check_set_regex(value)
        if checked is None:
            return
        self._blocklist = self._blocklist - checked
