import os
from dotenv import load_dotenv

load_dotenv()


BOT_TOKEN = os.environ.get('BOT_TOKEN')
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
GOOGLE_CSE_ID = os.environ.get('GOOGLE_CSE_ID')
OWNER_ID = int(os.environ.get('OWNER_ID'))
