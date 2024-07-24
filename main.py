#!/usr/bin/env python

"""
This module contains the main entry point of the application.
It imports necessary modules and sets up the environment.
"""

# -*- coding: utf-8 -*-

# pylint: disable=import-error
# from version import __version__
from log_handle import logger as log
from config_handler import result as config
import app

log.trace("Logging started")


if config['explicit-control']['enabled']:
    log.info("Explicit control enabled")
    match config['explicit-control']['type'].lower():
        case "web":
            log.info("Running in web mode")
            panelType: str = "web"
        case "cli":
            log.info("Running in cli (terminal) mode")
            panelType: str = "cli"
        case _:
            log.warning("Invalid explicit control mode, using cli (terminal) mode")
            log.info("Running in cli (terminal) mode")
            panelType: str = "cli"
else:
    log.info("Explicit control disabled")
    while 1:
        panelType = input("Enter 'web' for web mode, 'cli' for cli (terminal) mode: ").lower()
        if panelType in ["web", "cli"]:
            break
        log.warning("Invalid input, please enter 'web' or 'cli'")
    log.info(f"Running in {panelType} mode")

if panelType == "web":
    app.app.run(use_reloader=False, host="0.0.0.0", port=7171, threaded=True, debug=True)
else:
    log.info("More is not implemented yet (indev)")

    # raise NotImplementedError
