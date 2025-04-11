import os


DATABASE_CONNECTION_STRING = os.getenv("DATABASE_CONNECTION_STRING", "postgresql+asyncpg://chat:chat@db:5432/chat")