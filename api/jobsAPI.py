import flask
from flask import jsonify, request
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


@blueprint.route('/api/jobs', methods=['POST'])
def createJob():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not(all(key in request.json for key in ['teamLeader', 'job', 'workSize', 'collaborators', 'isFinished'])):
        return jsonify({'error': 'Bad request'})
    session = dbSession.createSession()
    job = Jobs(teamLeader=request.json['teamLeader'],
               job=request.json['job'],
               workSize=request.json['workSize'],
               collaborators=request.json['collaborators'],
               isFinished=request.json['isFinished'])
    if 'id' in request.json:
        if session.query(Jobs).get(request.json['id']):
            return jsonify({'error': 'Id already exists'})
        job.id = request.json['id']
    session.add(job)
    session.commit()
    return jsonify({'success': 'OK'})
