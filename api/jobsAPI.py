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
