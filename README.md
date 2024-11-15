# python3-cyberfusion-sway

Sway is an agent for [HAProxy agent health checks](https://cbonte.github.io/haproxy-dconv/2.4/configuration.html#agent-check).

Sway allows you to:

- Up/down servers based on commands (e.g. if a service is down)
- Distribute load efficiently: Sway dynamically sets [weight](https://docs.haproxy.org/2.6/configuration.html#weight), based on load.

# Install

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

## Start on servers

First, start Sway on the servers that HAProxy proxies traffic to.

### Manually

    ./start_server.py

### systemd

    systemctl start sway.service

## Configure in backend

Once Sway is running on your servers, tell HAProxy to use Sway for 'agent checks'.

For example:

    server server server.example.com:80 check agent-check agent-inter 5000 agent-port 60413 agent-send functional_service weight 100

In this example, `functional_service` corresponds to a check (see the [example configuration](examples/sway.yml).

### Note on weight

`Weight` **must** be set to at least 100 (as is the case in the example). Otherwise, the server could go down on high load.

The reason is as follows. Sway dynamically sets the weight of servers, which is a percentage of the weight set in the HAProxy config.

For example, if `weight 10` is set (default), and Sway returns a weight of 94% (= load of 5.1, rounded), the weight would be be 94% of 10 = 9.4.

However, HAProxy ignores decimals, so the weight will actually be 9. This is problematic when weight is less than 1: a weight of 0 means the server will effectively be down, as HAProxy then 'drains' it, meaning no new connections are accepted.

With a weight of at least 100, this can never happen (1% of 100 is 1, and Sway ensures that a lower percentage is never returned).
