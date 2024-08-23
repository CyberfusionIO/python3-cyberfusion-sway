"""A setuptools based setup module."""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="python3-cyberfusion-sway",
    version="1.0.9",
    description="Sway is an agent for HAProxy agent health checks.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Cyberfusion",
    author_email="support@cyberfusion.io",
    url="https://github.com/CyberfusionIO/python3-cyberfusion-sway",
    platforms=["linux"],
    packages=find_packages(
        include=[
            "sway",
            "sway.*",
        ]
    ),
    data_files=[],
    entry_points={"console_scripts": ["sway-server=sway.server:serve"]},
    install_requires=[
        "docopt==0.6.2",
        "PyYAML==5.3.1",
        "schema==0.7.5",
        "sdnotify==0.3.1",
    ],
)
