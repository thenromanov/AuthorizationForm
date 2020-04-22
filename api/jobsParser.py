from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('teamLeader', required=True)
parser.add_argument('job', required=True)
parser.add_argument('workSize', required=True)
parser.add_argument('collaborators', required=True)
parser.add_argument('isFinished', type=bool, required=True)
