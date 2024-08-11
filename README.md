# Sway

Sway is an agent for [HAProxy agent health checks](https://cbonte.github.io/haproxy-dconv/2.4/configuration.html#agent-check).

HAProxy supports two types of health checks:

- Regular health checks.
- Agent health checks. HAProxy connects to an agent. In this case, the agent is Sway. HAProxy tells Sway which checks to run. Sway then runs these check's commands. If at least one command's return code is not 0, Sway tells HAProxy to set the server state to 'down'.

# Install

## Generic

Run the following command to create a source distribution:

    python3 setup.py sdist

## Debian

Run the following commands to build a Debian package:

    mk-build-deps -i -t 'apt -o Debug::pkgProblemResolver=yes --no-install-recommends -y'
    dpkg-buildpackage -us -uc

The Debian package ships the following extras:

- systemd service
- System user that runs Sway
- sudoers file for generic Nagios scripts

Install the Debian package with `--no-install-suggests`. This prevents unneeded packages from being installed.

# Configure

Find example configs in `examples/`.

# Usage

## Start

### Manually

    ./start_server.py

### systemd

    systemctl start sway.service

# Tests

Run tests with pytest:

    pytest tests/

Note:

- The config file in `tests/sway.yml` is used.
