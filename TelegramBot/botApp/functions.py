import requests


def create_user(email, name, password, program_id):
    url = 'http://127.0.0.1:8000/program/user/'
    data = {
        "name": email,
        "email": name,
        "password": password,
    }
    response = requests.post(url, json=data)


def create_program(name,user_id):
    url = 'http://127.0.0.1:8000/program/'
    data = {
        "name": name,
        "user":user_id
    }
    response = requests.post(url, json=data)


def create_workout(name,program_id):
    url = 'http://127.0.0.1:8000/program/workout/'
    data = {
        "name": name,
        "programs":program_id
    }
    response = requests.post(url, json=data)


def create_load(weight, count, exercise_id, workout_id):
    url = 'http://127.0.0.1:8000/program/load/'
    data = {
        "weight": weight,
        "count":count,
        "exercise":exercise_id,
        "workout_id":workout_id,
    }
    response = requests.post(url, json=data)


def update_exercise(exercise_id, workout_id):
    url = f'http://127.0.0.1:8000/program/exercise/{exercise_id}/'
    data = {
        "workout":workout_id,
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.patch(url, json=data, headers=headers)
    print(response)
    return response