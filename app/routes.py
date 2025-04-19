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

        # Save to Redis
        r.zadd('leaderboard', {name: score})

        # Save to PostgreSQL
        result = Resume(name=name, score=score)
        db.session.add(result)
        db.session.commit()

        return jsonify({"message": "Resume analyzed successfully", "score": score}), 200

    return jsonify({"message": "Invalid file format"}), 400
