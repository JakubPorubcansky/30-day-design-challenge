import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SEND_NOTIFICATIONS = os.getenv('SEND_NOTIFICATIONS', 'false').lower() in ['true', '1', 'yes']