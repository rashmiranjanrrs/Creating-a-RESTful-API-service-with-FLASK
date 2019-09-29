from flask import Flask, request, jsonify
from app import db
from app.models import User, Task
from . import todo_api
from flask_httpauth import HTTPBasicAuth
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

auth = HTTPBasicAuth()

@auth.get_password
def pass_auth(username):
    user = User.query.filter_by(username=username).first()
    if user is not None:
        return user.password
    else:
        return None

@todo_api.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data['username']
    password_check = data['password']
    password = generate_password_hash(password_check)
    email = data['email']
    user = User(username, password, email)
    db.session.add(user)
    db.session.commit()
    return jsonify({
        'response': 'User ' + username + ' created successfully'
    })

@todo_api.route('/addtask', methods=['POST'])
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
@todo_api.route('/taskdone', methods=['GET'])
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

@todo_api.route('/deletetask', methods=['POST'])
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

@todo_api.route('/showtasks', methods=['GET'])
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
