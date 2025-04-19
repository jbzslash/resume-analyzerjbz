from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Resume(db.Model):
    __tablename__ = 'resumes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    upload_time = db.Column(db.DateTime, server_default=db.func.now())

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'score': self.score,
            'upload_time': self.upload_time.strftime('%Y-%m-%d %H:%M:%S')
        }
