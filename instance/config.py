import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-default-secret-key')
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your-openai-api-key')
