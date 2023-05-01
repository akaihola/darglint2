"""Common pytest fixtures for all test modules"""

import pytest

import darglint2.config


@pytest.fixture(autouse=True)
def default_config():
    # darglint2 automatically reads configuration from config files in the dev
    # environment. We must override config so that we maintain a controlled
    # test environment.
    darglint2.config._config = darglint2.config.Configuration.get_default_instance()
