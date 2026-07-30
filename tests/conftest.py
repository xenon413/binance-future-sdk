import os
from pathlib import Path
try:
    from dotenv import load_dotenv
except ImportError:
    pass
import pytest

@pytest.fixture(scope="session", autouse=True)
def load_env():
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        try:
            load_dotenv(env_path)
        except NameError:
            pass # dotenv not installed

@pytest.fixture(scope="session")
def api_credentials():
    return {
        "key": os.environ.get("BINANCE_API_KEY", "test_key"),
        "secret": os.environ.get("BINANCE_API_SECRET", "test_secret")
    }
