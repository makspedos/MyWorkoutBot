from aiogram.dispatcher.filters.state import State, StatesGroup


class AuthState(StatesGroup):
    AUTH_ENTER_EMAIL = State()
    AUTH_ENTER_NAME = State()
    AUTH_ENTER_PASSWORD = State()
    AUTH_CREATE = State()
    AUTH_SELECT_PROGRAM = State()
    USER_ACCOUNT = State()
    USER_WORKOUT_NAME = State()
    USER_CHOOSE_MUSCLE = State()
    USER_SELECT_EXERCISE = State()
    USER_ENTER_LOAD = State()
    USER_DELETE_WORKOUT = State()
