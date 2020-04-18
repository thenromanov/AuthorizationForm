import flask
from flask import jsonify
from data import dbSession
from data.jobs import Jobs


blueprint = flask.Blueprint('jobsAPI', __name__, template_folder='templates')


@blueprint.route('/api/jobs')
def getJobs():
    session = dbSession.createSession()
    jobs = session.query(Jobs).all()
    return jsonify(
        {
            'jobs': [item.to_dict(only=('teamLeader', 'job', 'workSize', 'collaborators', 'isFinished')) for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:id>', methods=['GET'])
def getJob(id):
    session = dbSession.createSession()
    job = session.query(Jobs).get(id)
    if job:
        return jsonify(
            {
                'jobs': job.to_dict(only=('teamLeader', 'job', 'workSize', 'collaborators', 'isFinished'))
            }
        )
    return jsonify({'error': 'Not found'})
