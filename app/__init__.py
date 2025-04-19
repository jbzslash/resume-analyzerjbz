from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import redis
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

# Initialize Redis connection
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Initialize SQLAlchemy
db = SQLAlchemy()

# Folder for uploading resumes
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    CORS(app)  # Enable Cross-Origin Resource Sharing

    # Ensure uploads folder exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
    # Load DB URL from environment
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize SQLAlchemy with app
    db.init_app(app)

    # Import and register blueprint
    from .routes import resume_bp
    app.register_blueprint(resume_bp)

    return app
