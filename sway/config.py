"""Config-related classes."""

import os
from typing import List

import yaml

from sway.checks import Check, CheckNotExistsError


def get_config_file_path() -> str:
    """Get config file path."""
    return os.environ["SWAY_CONFIG_FILE_PATH"]


class Config:
    """Represents YAML config."""

    def __init__(self) -> None:
        """Do nothing."""
        pass

    @property
    def checks(self) -> List[Check]:
        """Get checks."""
        result = []

        for name, values in self._settings["checks"].items():
            result.append(Check(name=name, command=values["command"]))

        return result

    @property
    def _settings(self) -> dict:
        """Get settings."""
        with open(get_config_file_path(), "rb") as fh:
            return yaml.load(fh.read(), Loader=yaml.SafeLoader)

    def get_check_by_name(self, *, name: str) -> Check:
        """Get check by name."""
        for check in self.checks:
            if check.name != name:
                continue

            return check

        raise CheckNotExistsError(name=name)

    @property
    def server_port(self) -> int:
        """Get server port."""
        return self._settings["server"]["port"]

    @property
    def server_host(self) -> str:
        """Get server host."""
        return self._settings["server"]["host"]

    @property
    def server_max_connections(self) -> int:
        """Get server max connections."""
        return self._settings["server"]["max_connections"]
