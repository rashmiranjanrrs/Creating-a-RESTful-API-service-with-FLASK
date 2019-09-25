#NAME: RASHMI RANJAN SAHOO
#PROJECT NAME: Creating a RESTful API service with FLASK
#Task Assinged Date: 23/09/2019 at 11:20 a.m
#Task End Date: 25/09/2019 at  06:30 p.m

from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.testing'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
auth = HTTPBasicAuth()


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

@auth.get_password
def get_pw(username):
    user = User.query.filter_by(username=username).first()
    if user is not None:
        return user.password
    else:
        return None

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data['username']
    password = data['password']
    email = data['email']
    user = User(username, password, email)
    db.session.add(user)
    db.session.commit()
    return jsonify({
        'response': 'User ' + username + ' created successfully'
    })

@app.route('/addtask', methods=['POST'])
@auth.login_required
def addtask():
    data = request.get_json()
    content = data['content']
    task = Task(content,user=User.query.filter_by(username=auth.username()).first())
    db.session.add(task)
    db.session.commit()
    return jsonify({
        'username': auth.username(),
        'task-id': task.id,
        'content': task.content
    })

@app.route('/deletetask', methods=['POST'])
@auth.login_required
def deletetask():
    data = request.get_json()
    task_id = data['task_id']
    task = Task.query.filter_by(id=task_id).first()
    if not task:
        return jsonify({'message' : 'No task found!'})

    deleted_task = jsonify({
        'status': 'success',
        'task_id': task.id,
        'content': task.content,
        'task_completed': task.done
    })
    db.session.delete(task)
    db.session.commit()
    return deleted_task

@app.route('/taskdone', methods=['GET'])
@auth.login_required
def markdone():
    data = request.get_json()
    task_id = data['task_id']
    task = Task.query.get(task_id)
    if task is None:
        return jsonify({
            'status': 'Failed'
        })
    task.done = True
    task.end_date = datetime.datetime.now()
    db.session.commit()
    return jsonify({
        'content': task.content,
        'add_date': task.add_date,
        'end_date': task.end_date,
        'task_completed': task.done
    })
db.create_all()

@app.route('/showtasks', methods=['GET'])
@auth.login_required
def alltasks():
    user = User.query.filter_by(username=auth.username()).first()
    if user is None:
        return jsonify({
            'status': 'failed'
        })
    task_list = {}
    for task in user.tasks:
        task_list[task.id] = {'content': task.content,
                              'add_date': task.add_date,
                              'task_completed': task.done}
    return jsonify(task_list)

db.create_all()
if __name__ == '__main__':
    app.run(debug=True)