import requests


def create_user():
    url = 'http://127.0.0.1:8000/program/user/'
    data = {
"name":"n",
"email":"e",
"password": "p",
"program" : 4
}
    response = requests.post(url, json=data)

    if response.status_code == 201:
        print('User created successfully.')
    else:
        print('Error creating user.')
        print(response)

if __name__ == '__main__':
    create_user()