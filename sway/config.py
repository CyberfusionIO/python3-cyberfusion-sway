"""Config-related classes."""

from typing import List

import yaml

from sway.checks import Check, CheckNotExistsError


class Config:
    """Represents YAML config."""

    def __init__(self, path: str) -> None:
        """Set attributes."""
        self.path = path

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
        with open(self.path, "rb") as fh:
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
