from flask import Flask
from flask_cors import CORS
import redis
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file for API keys

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def create_app():
    app = Flask(__name__)
    CORS(app)  # Allow frontend to talk to backend

    from .routes import resume_bp
    app.register_blueprint(resume_bp)

    return app
