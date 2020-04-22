from flask import jsonify
from flask_restful import abort, Resource
from data import dbSession
from data.jobs import Jobs
from .jobsParser import parser


def abortJob(id):
    session = dbSession.createSession()
    job = session.query(Jobs).get(id)
    if not job:
        abort(404, message=f'Job {id} not found')


class JobResource(Resource):
    def get(self, id):
        abortJob(id)
        session = dbSession.createSession()
        job = session.query(Jobs).get(id)
        return jsonify({'jobs': job.to_dict(only=('teamLeader', 'job', 'workSize', 'collaborators', 'isFinished'))})

    def delete(self, id):
        abortJob(id)
        session = dbSession.createSession()
        job = session.query(Jobs).get(id)
        session.delete(job)
        session.commit()
        return jsonify({'success': 'OK'})


class JobsResource(Resource):
    def get(self):
        session = dbSession.createSession()
        jobs = session.query(Jobs).all()
        return jsonify({'jobs': [item.to_dict(only=('teamLeader', 'job', 'workSize', 'collaborators', 'isFinished')) for item in jobs]})

    def post(self):
        args = parser.parse_args()
        session = dbSession.createSession()
        job = Jobs(teamLeader=args['teamLeader'],
                   job=args['job'],
                   workSize=args['workSize'],
                   collaborators=args['collaborators'],
                   isFinished=args['isFinished'])
        session.add(job)
        session.commit()
        return jsonify({'success': 'OK'})
