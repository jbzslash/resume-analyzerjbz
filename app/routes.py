from flask import Blueprint, request, jsonify
from .utils import extract_text_from_pdf, get_resume_score
from . import r

resume_bp = Blueprint('resume', __name__)

# ✅ Home Route — browser safe
@resume_bp.route('/', methods=['GET'])
def home():
    return "✅ Resume Analyzer Backend is Running!"

# 🧠 Resume Upload and Scoring
@resume_bp.route('/analyze', methods=['POST'])
def analyze():
    file = request.files['resume']
    name = request.form.get('name', 'Anonymous')

    text = extract_text_from_pdf(file)
    score = get_resume_score(text)

    r.zadd('leaderboard', {name: score})

    return jsonify({'name': name, 'score': score})

# 🏆 Leaderboard Route
@resume_bp.route('/leaderboard', methods=['GET'])
def leaderboard():
    data = r.zrevrange('leaderboard', 0, 9, withscores=True)
    return jsonify(data)

# 🧪 Test Route for Resume Upload and Scoring
@resume_bp.route('/test', methods=['POST'])
def test_resume():
    file = request.files['resume']
    text = extract_text_from_pdf(file)
    score = get_resume_score(text)
    return jsonify({'text': text, 'score': score})

# 🧪 Test Route for Redis Connectivity
@resume_bp.route('/test-redis_
