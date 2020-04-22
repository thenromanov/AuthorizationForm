from flask import jsonify
from flask_restful import abort, Resource
from data import dbSession
from data.users import User
from .usersParser import parser


def abortUser(id):
    session = dbSession.createSession()
    user = session.query(User).get(id)
    if not user:
        abort(404, message=f'User {id} not found')


class UserResource(Resource):
    def get(self, id):
        abortUser(id)
        session = dbSession.createSession()
        user = session.query(User).get(id)
        return jsonify({'users': user.to_dict(only=('surname', 'name', 'age', 'position', 'speciality', 'address', 'email'))})

    def delete(self, id):
        abortUser(id)
        session = dbSession.createSession()
        user = session.query(User).get(id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersResource(Resource):
    def get(self):
        session = dbSession.createSession()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict(only=('surname', 'name', 'age', 'position', 'speciality', 'address', 'email')) for item in users]})

    def post(self):
        args = parser.parse_args()
        session = dbSession.createSession()
        user = User(surname=args['surname'],
                    name=args['name'],
                    age=args['age'],
                    position=args['position'],
                    speciality=args['speciality'],
                    address=args['address'],
                    email=args['email'])
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})
