from requests import get, post, delete

print(post('http://localhost:5000/api/users').json())
print(post('http://localhost:5000/api/users', json={'name': 'Mark'}).json())
print(post('http://localhost:5000/api/users', json={'surname': 'Romanov',
                                                    'name': 'Nikita',
                                                    'age': 20,
                                                    'position': 'engineer',
                                                    'speciality': 'spec',
                                                    'address': 'module 1',
                                                    'email': 'nr@mail'}).json())
print(post('http://localhost:5000/api/users', json={'id': 1,
                                                    'surname': 'Romanov',
                                                    'name': 'Nikita',
                                                    'age': 20,
                                                    'position': 'engineer',
                                                    'speciality': 'spec',
                                                    'address': 'module 1',
                                                    'email': 'nr@mail'}).json())
print(get('http://localhost:5000/api/users').json())
print(get('http://localhost:5000/api/users/1').json())
print(get('http://localhost:5000/api/users/2').json())
print(delete('http://localhost:5000/api/users/99').json())
print(delete('http://localhost:5000/api/users/1').json())
print(get('http://localhost:5000/api/users').json())
