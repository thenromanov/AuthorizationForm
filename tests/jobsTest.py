from requests import get, post, delete

print(post('http://localhost:5000/api/jobs').json())
print(post('http://localhost:5000/api/jobs', json={'job': 'plant trees'}).json())
print(post('http://localhost:5000/api/jobs', json={'teamLeader': 1,
                                                   'job': 'plant trees',
                                                   'workSize': 15,
                                                   'collaborators': '2, 3',
                                                   'isFinished': False}).json())
print(get('http://localhost:5000/api/jobs').json())
print(get('http://localhost:5000/api/jobs/1').json())
print(get('http://localhost:5000/api/jobs/2').json())
print(delete('http://localhost:5000/api/jobs/99').json())
print(delete('http://localhost:5000/api/jobs/1').json())
print(get('http://localhost:5000/api/jobs').json())
