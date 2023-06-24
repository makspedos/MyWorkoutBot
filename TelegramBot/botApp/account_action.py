from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup
from .app import dp, bot
from .authorization import start
from .states import *
from .fetch import *
from .settings import urls

@dp.message_handler(commands=['account'], state=AuthState.USER_ACCOUNT)
async def account(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = data.get('user_id')
    inline_keyboard = InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Переглянути назву програми", callback_data=f'info_{user_id}')
    button2 = types.InlineKeyboardButton("Переглянути мої тренування", callback_data=f'program_{user_id}')
    button3 = types.InlineKeyboardButton("Вийти з аккаунту", callback_data=f'signout')
    inline_keyboard.add(button1, button2, button3)
    await bot.send_message(chat_id=message.chat.id, text='Обери', reply_markup=inline_keyboard)


@dp.callback_query_handler(lambda query: query.data == 'signout', state=AuthState.USER_ACCOUNT)
async def signout(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await start(callback_query.message, state)


@dp.callback_query_handler(lambda query: query.data.startswith('info_'), state=AuthState.USER_ACCOUNT)
async def program_info(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.data.split('_')[1]
    program_info = await get_simple_data(urls['program_by_user_id'],user_id)
    await state.update_data(program_id=program_info['id'])
    program_name = program_info['name']
    inline_keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = types.InlineKeyboardButton("Назад", callback_data='back')
    inline_keyboard.add(buttons)
    await bot.send_message(chat_id=callback_query.message.chat.id, text=program_name, reply_markup=inline_keyboard)


@dp.callback_query_handler(lambda query: query.data.startswith('program_'), state=AuthState.USER_ACCOUNT)
async def program_workouts(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.data.split('_')[1]
    program = await get_simple_data(urls['program_by_user_id'],user_id)
    await state.update_data(program_id=program['id'])
    workouts = await get_simple_data(urls['workout_by_program_id'],program['id'])
    inline_keyboard = InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton("Назад", callback_data='back')
    button2 = types.InlineKeyboardButton("Додати тренування?", callback_data='create_workout')
    #button3 = types.InlineKeyboardButton("Оновити тренування", callback_data=f'update_workout')
    button4 = types.InlineKeyboardButton("Видалити тренування", callback_data=f'delete_workout')
    button5 = types.InlineKeyboardButton("Переглянути прогрес вправ", callback_data=f'progress_{program["id"]}')

    if not workouts:
        inline_keyboard.add(button1, button2)
        await bot.send_message(chat_id=callback_query.message.chat.id, text='No workout`s yet',
                               reply_markup=inline_keyboard)
    else:
        str_return = ''
        for workout in workouts:
            exercises = await get_simple_data(urls['exercise_by_workout_id'], workout['id'])
            str_return += f"\n\n{workout['name']}  - день {str(workout['date'])}"
            for exercise in exercises:
                loads = await get_simple_data(urls['load_by_exercise_id_workout_id_program_id'],
                                              exercise['id'], workout['id'], program['id'])

                loads_str = ', '.join([f"{load['weight']}кг на {load['count']}" for load in loads])
                str_return += f"\n{exercise['name']} - {loads_str}"
        inline_keyboard.add(button1, button2, button4, button5)
        await callback_query.message.answer(str_return, reply_markup=inline_keyboard)


@dp.callback_query_handler(lambda query: query.data.startswith('progress_'), state=AuthState.USER_ACCOUNT)
async def exercise_progress(callback_query: types.CallbackQuery, state: FSMContext):
    program_id = callback_query.data.split('_')[1]

    str_return = ''

    exercises = await get_simple_data(urls['exercise_by_program_id'], program_id)

    for exercise in exercises:
        str_return += f"\n\n{exercise['name']}"
        loads = await get_simple_data(urls['load_by_exercise_id_program_id'], exercise['id'], program_id)
        loads_str = ', '.join([f"{load['weight']}кг на {load['count']}" for load in loads])
        str_return += f"\n{loads_str}"

    inline_keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = types.InlineKeyboardButton("Назад", callback_data='back')
    inline_keyboard.add(buttons)

    await bot.send_message(chat_id=callback_query.message.chat.id, text=str_return, reply_markup=inline_keyboard)


@dp.callback_query_handler(lambda query: query.data == 'back', state='*')
async def back(callback_query: types.CallbackQuery, state: FSMContext):
    await AuthState.USER_ACCOUNT.set()
    await account(callback_query.message, state)

