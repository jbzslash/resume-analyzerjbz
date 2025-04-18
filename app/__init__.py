
from flask import Flask
from flask_cors import CORS
import redis
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

# Redis connection setup
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Folder for uploading resumes
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    CORS(app)  # Enable Cross-Origin Resource Sharing for frontend-backend communication
    
    # Ensure uploads folder exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
    # Import routes and register blueprint
    from .routes import resume_bp
    app.register_blueprint(resume_bp)
    
    return app
