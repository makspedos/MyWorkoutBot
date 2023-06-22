from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup
from .app import dp, bot
from .states import AuthState
from .fetch import get_user, get_program
from .functions import *


@dp.message_handler(commands=['start'])
async def start(message: types.Message, state: FSMContext):
    inline_keyboard = InlineKeyboardMarkup(row_width=1)
    button_signup = types.InlineKeyboardButton('Signup', callback_data='signup')
    button_login = types.InlineKeyboardButton('Login', callback_data='login')
    inline_keyboard.add(button_signup, button_login)

    await message.answer('Welcome to the authentication process!', reply_markup=inline_keyboard)


@dp.callback_query_handler(lambda query: query.data in ['signup', 'login'])
async def authorization(callback_query: types.CallbackQuery, state: FSMContext):
    await AuthState.AUTH_ENTER_EMAIL.set()
    await state.update_data(selection=callback_query.data)
    await callback_query.message.answer('Enter email')


@dp.message_handler(state=AuthState.AUTH_ENTER_EMAIL)
async def enter_email(message: types.Message, state: FSMContext):
    email = message.text
    data = await state.get_data()
    selection = data.get('selection')

    if selection == 'signup':
        await AuthState.AUTH_ENTER_NAME.set()
        await message.answer('Email address validated. Please enter your name.')
    if selection == 'login':
        await AuthState.AUTH_ENTER_PASSWORD.set()
        await message.answer('Email address validated. Please enter your password.')
    await state.update_data(email=email)


@dp.message_handler(state=AuthState.AUTH_ENTER_NAME)
async def enter_name(message: types.Message, state: FSMContext):
    name = message.text
    await AuthState.AUTH_ENTER_PASSWORD.set()
    await state.update_data(name=name)
    await message.answer('Please enter your password.')


@dp.message_handler(state=AuthState.AUTH_ENTER_PASSWORD)
async def enter_password(message: types.Message, state: FSMContext):
    password = message.text
    await state.update_data(password=password)

    data = await state.get_data()
    selection = data.get('selection')
    email = data.get('email')
    password = data.get('password')

    if selection == 'signup':
        await AuthState.AUTH_SELECT_PROGRAM.set()
        await message.answer('Now, last thing. You need to name your program')

    if selection == 'login':
        try:
            user = await get_user(email, password)
            if user["email"] == email and user["password"] == password:
                await message.answer(f'Loged successfully.Hello {user["name"]}'
                                     f' Write /account to see information')

                program = await get_program(user['id'])
                await state.update_data(program_id=program['id'])

                await state.update_data(user_id=user['id'])
                await AuthState.USER_ACCOUNT.set()
        except:
            await message.answer('Error data. Write /start again')
            await state.finish()


@dp.message_handler(state=AuthState.AUTH_SELECT_PROGRAM)
async def enter_program(message: types.Message, state: FSMContext):
    program_name = message.text
    await state.update_data(program_name=program_name)

    data = await state.get_data()
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    create_user(email, name, password, program_name)
    user = await get_user(email,password)
    create_program(program_name,user['id'])
    await message.answer(f'Signup now ended. Type /start to go to the authorization menu')
    await state.finish()

