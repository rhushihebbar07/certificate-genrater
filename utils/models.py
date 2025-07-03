from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
# utils/models.py
from utils.extensions import db





# ✅ Team model
class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(100), nullable=False, unique=True)

    members = db.relationship('User', backref='team', lazy=True)
    project = db.relationship('Project', backref='team', uselist=False)
    quit_requests = db.relationship('QuitRequest', backref='team', lazy=True)


from flask_login import UserMixin
from datetime import datetime
from app import db
 # Change `yourapp` to the actual app filename if needed

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    class_batch = db.Column(db.String(100))
    age = db.Column(db.Integer)
    is_admin = db.Column(db.Boolean, default=False)
    role = db.Column(db.String(20), default='user')  # user, admin, lecturer
    profile_pic = db.Column(db.String(100), default='default.jpg')
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))

    sent_messages = db.relationship('TeamChat', backref='sender', lazy=True)
    quit_requests = db.relationship('QuitRequest', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'


# ✅ Project model
class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    file_path = db.Column(db.String(200))
    approved = db.Column(db.Boolean, default=False)

    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))

    def __repr__(self):
        return f'<Project {self.title}>'


# ✅ TeamChat model
class TeamChat(db.Model):
    __tablename__ = 'team_chats'

    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


# ✅ QuitRequest model
class QuitRequest(db.Model):
    __tablename__ = 'quit_requests'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    message = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<QuitRequest by User {self.user_id} for Team {self.team_id}>'
