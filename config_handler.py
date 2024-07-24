#!/usr/bin/env python

"""
This module contains the configuration handler.
It imports necessary modules and sets up the environment.
"""

# -*- coding: utf-8 -*-

import shutil

try:
    import tomllib
except (ModuleNotFoundError, ImportError):
    # noinspection PyPackageRequirements,PyUnresolvedReferences
    import tomli as tomllib
import sys

# pylint: disable=import-error
from version import __version__
from log_handle import logger as log


def init() -> dict:
    """
    This function initializes the configuration handler.

    :return: Dictionary containing the config data.
    """

    def caught(exception: Exception, critical: bool | int = False) -> None:
        """
        This function handles exceptions based on the critical flag.

        :param exception: The exception that was caught.
        :param critical: A flag indicating if the exception is critical.

        :return: None
        """
        if critical:
            log.error("We have caught an exception: " + str(exception))
            input("Press any key to exit...")
            sys.exit(1)
        else:
            log.error("We have caught an exception: " + str(exception))

    def bad_config() -> None:
        """
        A function that handles the configuration setup, if the config is invalid or corrupted.
        Prompts the user to create a new config file, renames the existing one if it exists,
        and provides instructions on editing the config file.

        :return: None
        """

        if input("Would you like to create a new config file?"
                 " If your config file already exists, it will be renamed to "
                 "config.toml.bak (y/n) ") == "y":
            try:
                shutil.move("user/config.toml", "./user/config.toml.bak")
                shutil.copyfile("resources/default_config.toml", "user/config.toml")
            except Exception as e:  # pylint: disable=broad-except
                caught(e, True)
            log.success("Created new default config file,"
                        " old config file renamed to config.toml.bak")
            log.info("Please edit config.toml to your liking")
        else:
            log.error("Exiting...")
            sys.exit()

    # loading config
    with open("user/config.toml", 'rb') as stream:
        try:
            config: dict = tomllib.load(stream)
        except tomllib.TOMLDecodeError as exc:
            caught(exc)
            bad_config()

        if config is None:
            caught("Config file is empty")
            bad_config()

        if 'config-version' not in list(config.keys()):
            caught("Config file is missing config-version")
            bad_config()

        if config['config-version'] != int(__version__.replace(".", "")):
            caught("Config version mismatch")
            bad_config()

        try:
            if not isinstance(config['token'], str) or \
                    not isinstance(config['explicit-control']['enabled'], bool) or \
                    not isinstance(config['explicit-control']['type'], str):
                caught("Config file is invalid")
                bad_config()
        except KeyError:
            caught("Config file is missing keys")
            bad_config()

        log.info("Config loaded")
        return config


result: dict = init()
