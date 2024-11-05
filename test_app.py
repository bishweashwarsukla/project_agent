import os
from dotenv import load_dotenv


def test_app():
    def _set_env():
        load_dotenv()

    assert os.environ["moneycontrol"] == "https://www.moneycontrol.com/"
