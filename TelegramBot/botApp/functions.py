import requests
from .settings import url_start

def create_user(email, name, password):
    url = f'{url_start}user/'
    data = {
        "name": name,
        "email": email,
        "password": password,
    }
    response = requests.post(url, json=data)


def create_program(name,user_id):
    url = f'{url_start}program/'
    data = {
        "name": name,
        "user":user_id
    }
    response = requests.post(url, json=data)


def create_workout(name,program_id):
    url = f'{url_start}workout/'
    data = {
        "name": name,
        "programs":program_id
    }
    response = requests.post(url, json=data)


def create_load(weight, count, exercise_id, workout_id, program_id):
    url = f'{url_start}load/'
    data = {
        "weight": weight,
        "count":count,
        "exercise":exercise_id,
        "workout_id":workout_id,
        "program_id":program_id,
    }
    response = requests.post(url, json=data)


def update_exercise(exercise_id, workout_id):
    url = f'{url_start}exercise/{exercise_id}/'
    data = {
        "workout":workout_id,
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.patch(url, json=data, headers=headers)
    return response


def delete_workout(workout_name, program_id):
    url = f'{url_start}workout/program/{program_id}/{workout_name}/'
    response = requests.delete(url)


def update_exercise(exercise_id, workout_id):
    url = f'{url_start}exercise/{exercise_id}/'
    data = {
        "workout":workout_id,
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.patch(url, json=data, headers=headers)
    return response

