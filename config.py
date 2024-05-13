from os import getenv
from dotenv import load_dotenv

load_dotenv()

TOKEN = getenv("BOT_TOKEN")
DATA_PATH = getenv("DATA_PATH")
# ADMIN_IDS = [getenv('ADMIN_IDS')]
# TARGET_CHAT_IDS = [getenv('TARGET_CHAT_IDS')]
# DISCUSSION_CHAT_ID = [getenv('DISCUSSION_CHAT_ID')]
# SECONDARY_CHAT_ID = getenv('SECONDARY_CHAT_ID')
# YANDEX_PASSPORT_OAUTH_TOKEN = getenv('YANDEX_PASSPORT_OAUTH_TOKEN')
# OPENAI_KEY = getenv('OPENAI_KEY')
# MONGODB_DBNAME = getenv('MONGODB_DBNAME')
