# settings.py
from dotenv import load_dotenv

# OR, explicitly providing path to '.env'
from pathlib import Path  # python3 only
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

import os
BASE_PATH = os.getenv("BASE_PATH")
