from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./sinapi.db",
)

engine = create_engine(DATABASE_URL,echo=True)