# Sway

Sway is an agent for [HAProxy agent health checks](https://cbonte.github.io/haproxy-dconv/2.4/configuration.html#agent-check).

HAProxy supports two types of health checks:

- Regular health checks.
- Agent health checks. HAProxy connects to an agent. In this case, the agent is Sway. HAProxy tells Sway which checks to run. Sway then runs these check's commands. If at least one command's return code is not 0, Sway tells HAProxy to set the server state to 'down'.

# Config

Find example configs in `examples/`.

# Start

Start Sway manually with:

    ./start_server.py

Installed the Debian package? Use systemd:

    systemctl start sway.service

# Build

Build Sway yourself.

## Generic

Run the following command to create a source distribution:

    python3 setup.py sdist

## Debian

Run the following commands to build a Debian package:

    mk-build-deps -i -t 'apt -o Debug::pkgProblemResolver=yes --no-install-recommends -y'
    dpkg-buildpackage -us -uc

The Debian package comes with at least the following extras:

- systemd service
- System user that runs Sway
- sudoers file for generic Nagios scripts

Install the Debian package with `--no-install-suggests`. This prevents unneeded packages from being installed.

# Tests

Run tests with pytest:

    pytest tests/

The config file in `tests/sway.yml` is used. The `SWAY_CONFIG_FILE_PATH` environment variable is ignored.
