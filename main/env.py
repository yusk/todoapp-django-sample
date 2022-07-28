import os

from dotenv import load_dotenv

load_dotenv()

CORS_ORIGIN_WHITELIST = list(
    os.environ.get('CORS_ORIGIN_WHITELIST',
                   'http://localhost:3000,http://127.0.0.1:3000').split(','))
