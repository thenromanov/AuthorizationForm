import flask
from flask import jsonify, request
from data import dbSession
from data.users import User

blueprint = flask.Blueprint('usersAPI', __name__, template_folder='templates')


@blueprint.route('/api/users')
def getUsers():
    session = dbSession.createSession()
    users = session.query(User).all()
    return jsonify(
        {
            'users': [item.to_dict(only=('surname', 'name', 'age', 'position', 'speciality', 'address', 'email')) for item in users]
        }
    )


@blueprint.route('/api/users/<int:id>', methods=['GET'])
def getUser(id):
    session = dbSession.createSession()
    user = session.query(User).get(id)
    if user:
        return jsonify(
            {
                'users': user.to_dict(only=('surname', 'name', 'age', 'position', 'speciality', 'address', 'email'))
            }
        )
    return jsonify({'error': 'Not found'})


@blueprint.route('/api/users', methods=['POST'])
def createUser():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not(all(key in request.json for key in ['surname', 'name', 'age', 'position', 'speciality', 'address', 'email'])):
        return jsonify({'error': 'Bad request'})
    session = dbSession.createSession()
    user = User(surname=request.json['surname'],
                name=request.json['name'],
                age=request.json['age'],
                position=request.json['position'],
                speciality=request.json['speciality'],
                address=request.json['address'],
                email=request.json['email'])
    if 'id' in request.json:
        if session.query(User).get(request.json['id']):
            return jsonify({'error': 'Id already exists'})
        user.id = request.json['id']
    session.add(user)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:id>', methods=['DELETE'])
def deleteUser(id):
    session = dbSession.createSession()
    user = session.query(User).get(id)
    if not user:
        return jsonify({'error': 'Not found'})
    session.delete(user)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:id>', methods=['PUT'])
def editUser(id):
    session = dbSession.createSession()
    user = session.query(User).get(id)
    if not user:
        return jsonify({'error': 'Not found'})
    elif not request.json:
        return jsonify({'error': 'Bad request'})
    user.surname = request.json.get('surname', user.surname)
    user.name = request.json.get('name', user.name)
    user.age = request.json.get('age', user.age)
    user.position = request.json.get('position', user.position)
    user.speciality = request.json.get('speciality', user.speciality)
    user.address = request.json.get('address', user.address)
    user.email = request.json.get('email', user.email)
    session.commit()
    return jsonify({'success': 'OK'})
