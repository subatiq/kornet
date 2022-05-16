from distutils.core import setup

from setuptools import find_packages

all_packages = find_packages()

setup(
    name="kornet",
    packages=all_packages,
    version="0.0.15",
    license="MIT",
    description="A library for mass execution of ssh commands on remote machines fleet.",
    author="Vladimir Semenov",
    author_email="subatiq@gmail.com",
    url="https://github.com/subatiq/kornet",
    download_url="https://github.com/subatiq/kornet/archive/refs/tags/pre-0.0.15.tar.gz",
    keywords=["ssh", "automation", "orchestration"],
    install_requires=[
        "paramiko",
        "asyncssh",
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
