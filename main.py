#!/usr/bin/env python

"""
This module contains the main entry point of the application.
It imports necessary modules and sets up the environment.
"""

# -*- coding: utf-8 -*-

import app
from config_handler import result as config

# pylint: disable=import-error
# from version import __version__
from log_handle import logger as log

log.trace("Logging started")

if config["explicit-control"]["enabled"]:
    log.info("Explicit control enabled")
    PANEL_TYPE: str = ""
    log.trace(f'PANEL_TYPE is set to "{PANEL_TYPE}" in explicit control mode')
    match config["explicit-control"]["type"].lower():
        case "web":
            PANEL_TYPE = "web"
        case "cli":
            PANEL_TYPE = "cli"
        case _:
            log.warning("Invalid explicit control mode, using cli (terminal) mode")
            PANEL_TYPE = "cli"

    log.info(f"Running in {PANEL_TYPE} mode")
else:
    log.info("Explicit control disabled")
    while 1:
        PANEL_TYPE = input("Enter 'web' for web mode, 'cli' for cli (terminal) mode: ").lower()
        if PANEL_TYPE in ["web", "cli"]:
            break
        log.warning("Invalid input, please enter 'web' or 'cli'")
    log.info(f"Running in {PANEL_TYPE} mode")

if PANEL_TYPE == "web":
    app.app.run(use_reloader=False, host="0.0.0.0", port=7171, threaded=True, debug=True)
else:
    log.info("More is not implemented yet (indev)")

    # raise NotImplementedError
