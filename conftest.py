"""
This module contains pytest configuration and fixtures.
"""
import pytest


def pytest_addoption(parser):
    """
    Adds --token command line option to pytest.
    This option is used to specify the Telegram bot token.
    """
    parser.addoption("--token", action="store")


@pytest.fixture(scope='session')
def token(request) -> str:
    """
    Fixture that returns the Telegram bot token.

    :param request: The pytest request object.
    :type request: _pytest.fixtures.FixtureRequest
    :return: The Telegram bot token. If the token is not provided, it skips the test.
    :rtype: str
    """
    token_value = request.config.option.token
    if token_value is None:
        token_value = pytest.mark.skip(reason="No token provided")
    return token_value
