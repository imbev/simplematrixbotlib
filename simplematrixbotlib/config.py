from dataclasses import dataclass, field
import toml
import re

@dataclass
class Config:
    _join_on_invite: bool = True
    _allowlist: set[str] = field(default_factory=set)  #TODO: default to bot's homeserver
    _blocklist: set[str] = field(default_factory=set)

    def _check_set_regex(self, value: set[str]) -> set[re.Pattern]:
        new_list = set()
        # loop value
        for v in value:
            # try re.compile
            try:
                tmp = re.compile(v)
            # except return False
            except re.error:
                print(f"{v} is not a valid regular expression. Ignoring your list update.")
                return
            new_list.add(tmp)
        return new_list

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
    def allowlist(self) -> set[str]:
        """
        Returns
        -------
        set[str]
            A set of strings which represent Matrix IDs or a regular expression matching Matrix IDs.
            Can be used in conjunction with blocklist to check if the sender is allowed to issue a command to the bot.
            An empty set implies that everyone is allowed.
        """
        return self._allowlist

    @allowlist.setter
    def allowlist(self, value: set[str]) -> None:
        # TODO rebase onto new master with working pytest
        checked = self._check_set_regex(value)
        if checked is None:
            return
        self._allowlist = checked

    def add_allowlist(self, value: set[str]) -> None:
        """
        Parameters
        ----------
        value : set[str]
            A set of strings which represent Matrix IDs or a regular expression matching Matrix IDs to be added to allowlist.
        """
        checked = self._check_set_regex(value)
        if checked is None:
            return
        self._allowlist = self._allowlist.union(checked)

    def remove_allowlist(self, value: set[str]) -> None:
        """
        Parameters
        ----------
        value : set[str]
            A set of strings which represent Matrix IDs or a regular expression matching Matrix IDs to be removed from allowlist.
        """
        checked = self._check_set_regex(value)
        if checked is None:
            return
        self._allowlist = self._allowlist - checked

    @property
    def blocklist(self) -> set[str]:
        """
        Returns
        -------
        set[str]
            A set of strings which represent Matrix IDs or a regular expression matching Matrix IDs.
            Can be used in conjunction with allowlist to check if the sender is disallowed to issue a command to the bot.
        """
        return self._blocklist

    @blocklist.setter
    def blocklist(self, value: set[str]) -> None:
        checked = self._check_set_regex(value)
        if checked is None:
            return
        self._blocklist = checked

    def add_blocklist(self, value: set[str]) -> None:
        """
        Parameters
        ----------
        value : set[str]
            A set of strings which represent Matrix IDs or a regular expression matching Matrix IDs to be added to blocklist.
        """
        checked = self._check_set_regex(value)
        if checked is None:
            return
        self._blocklist = self._blocklist.union(checked)

    def remove_blocklist(self, value: set[str]) -> None:
        """
        Parameters
        ----------
        value : set[str]
            A set of strings which represent Matrix IDs or a regular expression matching Matrix IDs to be removed from blocklist.
        """
        checked = self._check_set_regex(value)
        if checked is None:
            return
        self._blocklist = self._blocklist - checked
