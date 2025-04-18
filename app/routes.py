from flask import Blueprint, request, jsonify
from .utils import extract_text_from_pdf, get_resume_score
from . import r
from werkzeug.utils import secure_filename

resume_bp = Blueprint('resume', __name__)

ALLOWED_EXTENSIONS = {'pdf', 'docx'}

def allowed_file(filename):
    """Check if the file is of an allowed type (pdf or docx)."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@resume_bp.route('/', methods=['GET'])
def home():
    """Home route to check if the backend is running."""
    return "✅ Resume Analyzer Backend is Running!"

@resume_bp.route('/analyze', methods=['POST'])
def analyze():
    """Route to handle resume upload, text extraction, and scoring."""
    if 'resume' not in request.files:
        return jsonify({"message": "No resume file found"}), 400
    
    file = request.files['resume']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        text = extract_text_from_pdf(file)  # Extract text from resume
        score = get_resume_score(text)  # Get score for the resume
        
        name = request.form.get('name', 'Anonymous')
        r.zadd('leaderboard', {name: score})  # Add to Redis leaderboard
        
        return jsonify({'name': name, 'score': score, 'message': 'File uploaded successfully!'}), 200
    else:
        return jsonify({"message": "Invalid file type"}), 400

@resume_bp.route('/leaderboard', methods=['GET'])
def leaderboard():
    """Route to display the leaderboard from Redis."""
    data = r.zrevrange('leaderboard', 0, 9, withscores=True)
    return jsonify(data)

@resume_bp.route('/test', methods=['POST'])
def test_resume():
    """Route for testing resume upload and scoring."""
    if 'resume' not in request.files:
        return jsonify({"message": "No resume file found"}), 400
    
    file = request.files['resume']
    text = extract_text_from_pdf(file)  # Extract text from resume
    score = get_resume_score(text)  # Get score
    
    return jsonify({'text': text, 'score': score})

@resume_bp.route('/test-redis', methods=['GET'])
def test_redis():
    """Route to test Redis connectivity."""
    try:
        r.set('test_key', 'test_value')
        return jsonify({"message": "Redis is working fine!"}), 200
    except:
        return jsonify({"message": "Redis is not working!"}), 500
