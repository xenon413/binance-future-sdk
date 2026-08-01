import os
from pathlib import Path
try:
    from dotenv import load_dotenv
except ImportError:
    pass
import pytest

@pytest.fixture(scope="session", autouse=True)
def logging_config():
    pass

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
