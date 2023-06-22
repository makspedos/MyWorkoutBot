import aiohttp
from .settings import PROGRAM_API_URL_ALL


async def get_program(user_id=None):
    async with aiohttp.ClientSession() as session:
        if user_id is None:
            async with session.get('http://127.0.0.1:8000/program/') as response:
                programs = await response.json()
        else:
            async with session.get(f'http://127.0.0.1:8000/program/{user_id}/') as response:
                programs = await response.json()
        return programs


async def get_workout(program_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://127.0.0.1:8000/program/{program_id}/exercise/workout/') as response:
            workouts = await response.json()
            return workouts


async def get_user(email,password):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://127.0.0.1:8000/program/user/{email}/{password}/') as response:
            user = await response.json()
            return user


async def get_muscle(muscle_id=None):
    async with aiohttp.ClientSession() as session:
        if muscle_id is None:
            async with session.get(f'http://127.0.0.1:8000/program/muscle/') as response:
                muscles = await response.json()
        else:
            async with session.get(f'http://127.0.0.1:8000/program/muscle/{muscle_id}') as response:
                muscles = await response.json()
        return muscles


async def get_exercises_by_muscle(muscle_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://127.0.0.1:8000/program/exercise/muscle/{muscle_id}/') as response:
            exercises = await response.json()
            return exercises

async def get_exercises_by_workout(workout_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://127.0.0.1:8000/program/exercise/workout/{workout_id}/') as response:
            exercises = await response.json()
            return exercises

async def get_loads(exercise_id,workout_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://127.0.0.1:8000/program/load/{exercise_id}/{workout_id}') as response:
            loads = await response.json()
            return loads