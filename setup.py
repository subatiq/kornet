from distutils.core import setup

from setuptools import find_packages

all_packages = find_packages()

setup(
    name="chieftane",
    packages=all_packages,
    version="0.0.2",
    license="MIT",
    description="A library for mass execution of ssh commands on remote machines fleet.",
    author="Vladimir Semenov",
    author_email="subatiq@gmail.com",
    url="https://github.com/subatiq/chieftane",
    download_url="https://github.com/subatiq/chieftane/archive/refs/tags/pre-0.0.0.tar.gz",
    keywords=["SSH", "AUTOMATION", "ORCHESTRATION"],
    install_requires=[
        "paramiko",
        "pydantic",
        "pyyaml",
        "loguru",
        "typer",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: System Administrators",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
    ],
)
