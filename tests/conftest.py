import os
import logging
from pathlib import Path
from dotenv import load_dotenv
import pytest

@pytest.fixture(scope="session", autouse=True)
def logging_config():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(created)f | %(asctime)s | %(name)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S %z",
        filemode="w",
        filename="test_run.log",
        force=True
    )

@pytest.fixture(scope="session", autouse=True)
def load_env():
    env_path = r"tests\data\.env"
    load_dotenv(env_path)

@pytest.fixture(scope="session")
def api_credentials():
    return {
        "key": os.environ.get("BINANCE_TEST_API_KEY", "test_key"),
        "secret": os.environ.get("BINANCE_TEST_API_SECRET", "test_secret")
    }
