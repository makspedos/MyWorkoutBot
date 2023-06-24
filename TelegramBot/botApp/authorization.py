from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup
from .app import dp
from .states import AuthState
from .fetch import get_simple_data
from .functions import *
from .settings import urls

@dp.message_handler(commands=['start'])
async def start(message: types.Message, state: FSMContext):
    inline_keyboard = InlineKeyboardMarkup(row_width=1)
    button_signup = types.InlineKeyboardButton('Створити аккаунт', callback_data='signup')
    button_login = types.InlineKeyboardButton('Увійти', callback_data='login')
    inline_keyboard.add(button_signup, button_login)

    await message.answer('Авторизуйтесь', reply_markup=inline_keyboard)


@dp.callback_query_handler(lambda query: query.data in ['signup', 'login'])
async def authorization(callback_query: types.CallbackQuery, state: FSMContext):
    await AuthState.AUTH_ENTER_EMAIL.set()
    await state.update_data(selection=callback_query.data)
    await callback_query.message.answer('Уведіть почту')


@dp.message_handler(state=AuthState.AUTH_ENTER_EMAIL)
async def enter_email(message: types.Message, state: FSMContext):
    email = message.text
    data = await state.get_data()
    selection = data.get('selection')

    if selection == 'signup':
        await AuthState.AUTH_ENTER_NAME.set()
        await message.answer('Далі ім`я.')
    if selection == 'login':
        await AuthState.AUTH_ENTER_PASSWORD.set()
        await message.answer('Пароль.')
    await state.update_data(email=email)


@dp.message_handler(state=AuthState.AUTH_ENTER_NAME)
async def enter_name(message: types.Message, state: FSMContext):
    name = message.text
    await AuthState.AUTH_ENTER_PASSWORD.set()
    await state.update_data(name=name)
    await message.answer('Вигадайте пароль.')


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
        await message.answer('Остання річ - назвіть свою програму тренувань')

    if selection == 'login':
        try:
            user = await get_simple_data(urls['user_by_data'], email, password)
            print(user)
            if user["email"] == email and user["password"] == password:
                await message.answer(f'Було зайдено до акаунту.Привіт, {user["name"]},'
                                     f' Уведіть /account , щоб переглянути інформаціі в акаунті')

                program = await get_simple_data(urls['program_by_user_id'],user['id'])
                await state.update_data(program_id=program['id'])

                await state.update_data(user_id=user['id'])
                await AuthState.USER_ACCOUNT.set()
        except:
            await message.answer('Дані невірні. Напишіть /start знову')
            await state.finish()


@dp.message_handler(state=AuthState.AUTH_SELECT_PROGRAM)
async def enter_program(message: types.Message, state: FSMContext):
    program_name = message.text
    await state.update_data(program_name=program_name)
    data = await state.get_data()
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    create_user(email, name, password)
    user = await get_simple_data(urls['user_by_data'], email,password)
    create_program(program_name,user['id'])
    await message.answer(f'Реєстрація завершена. Напишіть /start ,щоб обрати авторизацію')
    await state.finish()

