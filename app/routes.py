from flask import Blueprint, request, jsonify
from .utils import extract_text_from_pdf, get_resume_score
from . import r, db
from .models import Resume
from werkzeug.utils import secure_filename

resume_bp = Blueprint('resume', __name__)

ALLOWED_EXTENSIONS = {'pdf', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@resume_bp.route('/', methods=['GET'])
def home():
    return "✅ Resume Analyzer Backend is Running!"

@resume_bp.route('/analyze', methods=['POST'])
def analyze():
    if 'resume' not in request.files:
        return jsonify({"message": "No resume file found"}), 400

    file = request.files['resume']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    if file and allowed_file(file.filename):
        text = extract_text_from_pdf(file)
        score = get_resume_score(text)
        name = request.form.get('name', 'Anonymous')

        try:
            # Save to Redis leaderboard
            r.zadd('leaderboard', {name: score})
        except Exception as e:
            return jsonify({"message": f"Error saving to Redis: {str(e)}"}), 500

        # Save to PostgreSQL database
        result = Resume(name=name, score=score)
        db.session.add(result)
        db.session.commit()

        return jsonify({"message": "Resume analyzed successfully", "score": score}), 200

    return jsonify({"message": "Invalid file format"}), 400
