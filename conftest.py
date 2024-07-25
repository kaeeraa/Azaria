import pytest


def pytest_addoption(parser):
    parser.addoption("--token", action="store")


@pytest.fixture(scope='session')
def token(request):
    token_value = request.config.option.token
    if token_value is None:
        token_value = pytest.mark.skip(reason="No token provided")
    return token_value
