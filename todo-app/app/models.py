from app import db
import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    add_date = db.Column(db.DateTime, default=datetime.datetime.now())
    end_date = db.Column(db.DateTime)
    done = db.Column(db.Boolean, default=False)
    user = db.relationship('User', backref='tasks', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), default=False)
    def __init__(self, content, user):
        self.content = content
        self.user = user

    def __repr__(self):
        return '<Task %r>' % self.content