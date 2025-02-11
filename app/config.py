import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

SHIPAY_ACCESS_KEY = os.getenv("SHIPAY_ACCESS_KEY")
SHIPAY_CLIENT_ID = os.getenv("SHIPAY_CLIENT_ID")
SHIPAY_SECRET_KEY = os.getenv("SHIPAY_SECRET_KEY")
SHIPAY_BASE_URL = os.getenv("SHIPAY_BASE_URL")
CALLBACK_URL = os.getenv("CALLBACK_URL")
WORKER_INTERVAL_SECONDS = int(os.getenv("WORKER_INTERVAL_SECONDS", 15))
