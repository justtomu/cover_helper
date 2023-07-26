import os
from pathlib import Path

from dotenv.main import load_dotenv

load_dotenv(str(Path(__file__).parent.parent.parent / '.env'))

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
BARD_TOKEN = os.getenv('BARD_TOKEN')
REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = os.getenv('REDIS_PORT', '6379')

