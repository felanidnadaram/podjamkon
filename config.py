import os
from dotenv import load_dotenv
from pathlib import Path

# مسیر قطعی به فایل .env در ریشه پروژه
env_path = Path(__file__).parent.parent / '.env'   # bot/config.py -> ../.env
load_dotenv(dotenv_path=env_path)


print("S3_BUCKET =", os.getenv("S3_BUCKET"))
print("TELEGRAM_BOT_TOKEN =", os.getenv("TELEGRAM_BOT_TOKEN"))


load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")
S3_ENDPOINT = os.getenv("S3_ENDPOINT")
S3_BUCKET = os.getenv("S3_BUCKET")

# Validate required variables
required = [
    "TELEGRAM_BOT_TOKEN", "DATABASE_URL", "S3_ACCESS_KEY",
    "S3_SECRET_KEY", "S3_ENDPOINT", "S3_BUCKET"
]
for var in required:
    if not locals().get(var):
        raise ValueError(f"Environment variable {var} is not set")