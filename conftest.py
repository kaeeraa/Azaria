"""
This module contains pytest configuration and fixtures.
"""

import pytest
from black import Any


def pytest_addoption(parser: pytest.Parser) -> object:
    """
    Adds --token command line option to pytest.
    This option is used to specify the Telegram bot token.

    :param parser:
    :rtype: object
    """
    parser.addoption("--token", action="store")

    return parser


@pytest.fixture(scope="session")
def token(request: pytest.FixtureRequest) -> Any:
    """
    Fixture that returns the Telegram bot token.

    :return: The Telegram bot token.
    :param request: The pytest request object.
    :type request: _pytest.fixtures.FixtureRequest
    :return: The Telegram bot token. If the token is not provided, it skips the test.
    :rtype: Any
    """
    token_value = request.config.option.token
    if token_value is None:
        token_value = pytest.mark.skip(reason="No token provided")
    return token_value
