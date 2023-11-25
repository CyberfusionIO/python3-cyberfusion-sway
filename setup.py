"""A setuptools based setup module."""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sway",
    version="1.0.6",
    description="Sway is an agent for HAProxy agent health checks.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    author="William Edwards",
    author_email="support@cyberfusion.nl",
    url="https://github.com/CyberfusionIO/sway",
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
        "PyYAML>=3.13",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=["cyberfusion", "haproxy"],
    license="MIT",
)
