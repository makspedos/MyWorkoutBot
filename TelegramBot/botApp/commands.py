from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup
from .app import dp, bot
from .states import *
from .fetch import *
from .functions import create_load, create_workout,update_exercise


@dp.message_handler(commands=['account'], state=AuthState.USER_ACCOUNT)
async def account(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = data.get('user_id')
    inline_keyboard = InlineKeyboardMarkup()

    buttons = types.InlineKeyboardButton("Watch program", callback_data=f'info_{user_id}')
    workout_button = types.InlineKeyboardButton("Watch workouts", callback_data=f'program_{user_id}')
    inline_keyboard.add(buttons, workout_button)

    await bot.send_message(chat_id=message.chat.id, text='Select', reply_markup=inline_keyboard)


@dp.callback_query_handler(lambda query: query.data.startswith('info_'), state=AuthState.USER_ACCOUNT)
async def program_info(callback_query: types.CallbackQuery, state: FSMContext):
    id = callback_query.data.split('_')[1]
    program_info = await get_program(id)
    await state.update_data(program_id=program_info['id'])
    program_name = program_info['name']
    inline_keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = types.InlineKeyboardButton("Back", callback_data='back')
    inline_keyboard.add(buttons)
    await bot.send_message(chat_id=callback_query.message.chat.id, text=program_name, reply_markup=inline_keyboard)


@dp.callback_query_handler(lambda query: query.data.startswith('program_'), state=AuthState.USER_ACCOUNT)
async def program_workouts(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.data.split('_')[1]
    program = await get_program(user_id)
    await state.update_data(program_id=program['id'])
    workouts = await get_workout(program['id'])


    inline_keyboard = InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton("Back", callback_data='back')
    button2 = types.InlineKeyboardButton("Add workout?", callback_data='create_workout')
    button3 = types.InlineKeyboardButton("Update workout", callback_data=f'update_workout')
    inline_keyboard.add(button1, button2, button3)

    if not workouts:
        await bot.send_message(chat_id=callback_query.message.chat.id, text='No workout`s yet',
                               reply_markup=inline_keyboard)
    else:
        str_return = ''
        for workout in workouts:
            exercises = await get_exercises_by_workout(workout['id'])
            str_return += f"\n\n{workout['name']}  - день {str(workout['date'])}"

            for exercise in exercises:
                loads = await get_loads(exercise['id'], workout['id'])
                loads_str = ', '.join([f"{load['weight']} на {load['count']}" for load in loads])
                str_return += f"\n{exercise['name']} - {loads_str}"

        await bot.send_message(chat_id=callback_query.message.chat.id, text=str_return,
                               reply_markup=inline_keyboard)


@dp.callback_query_handler(lambda query: query.data == 'create_workout', state=AuthState.USER_ACCOUNT)
async def workout_create(callback_query: types.CallbackQuery, state: FSMContext):
    await AuthState.USER_WORKOUT_NAME.set()
    await callback_query.message.answer('Дай назву тренуванню')
    new_workout = True
    await state.update_data(new_workout=new_workout)


@dp.callback_query_handler(lambda query: query.data == 'create_workout', state=AuthState.USER_ACCOUNT)
async def workout_create(callback_query: types.CallbackQuery, state: FSMContext):
    await AuthState.USER_WORKOUT_NAME.set()
    await callback_query.message.answer('Дай назву тренуванню')
    new_workout = True
    await state.update_data(new_workout=new_workout)


@dp.message_handler(state=AuthState.USER_WORKOUT_NAME)
async def workout_name(message: types.Message, state: FSMContext):
    await AuthState.USER_CHOOSE_MUSCLE.set()
    data = await state.get_data()
    new_workout=data.get('new_workout')
    program_id = data.get('program_id')

    if new_workout == True:
        workout_name = message.text
        await state.update_data(workout_name=workout_name)
        create_workout(workout_name, program_id)


    muscles = await get_muscle()

    inline_keaboard = InlineKeyboardMarkup()
    buttons = [types.InlineKeyboardButton(muscle['name'], callback_data=f'muscle_{muscle["id"]}') for muscle in muscles]
    inline_keaboard.add(*buttons)
    await message.answer('Обери м`яз,на яку буде вправа', reply_markup=inline_keaboard)


@dp.callback_query_handler(lambda query: query.data.startswith('muscle_'), state=AuthState.USER_CHOOSE_MUSCLE)
async def muscle_select(callback_query: types.CallbackQuery, state: FSMContext):
    muscle_id = callback_query.data.split('_')[1]
    exercises = await get_exercises_by_muscle(muscle_id)
    await AuthState.USER_SELECT_EXERCISE.set()
    inline_keaboard = InlineKeyboardMarkup()
    buttons = [types.InlineKeyboardButton(exercise['name'], callback_data=f'exercise_{exercise["id"]}') for exercise in
               exercises]

    inline_keaboard.add(*buttons)

    await callback_query.message.answer('Обери вправу', reply_markup=inline_keaboard)


@dp.callback_query_handler(lambda query: query.data.startswith('exercise_'), state=AuthState.USER_SELECT_EXERCISE)
async def exercise_select(callback_query: types.CallbackQuery, state: FSMContext):
    exercise_id = int(callback_query.data.split('_')[1])
    data = await state.get_data()
    program_id = data.get('program_id')
    workout = await get_workout(program_id)
    workout_id = workout[-1]['id']

    print('workout_id' + str(workout_id) + '\t' + str(exercise_id))
    await state.update_data(workout_id=workout_id)

    update_exercise(exercise_id, workout_id)
    await state.update_data(exercise_id=exercise_id)
    await AuthState.USER_ENTER_LOAD.set()
    await callback_query.message.answer('Enter weight and reps like: 115/8, 100/2 ...')


@dp.message_handler(state=AuthState.USER_ENTER_LOAD)
async def load_process(message: types.Message, state: FSMContext):
    loads = message.text
    loads = loads.split(', ')
    return_load = [load.split('/') for load in loads]

    data = await state.get_data()
    exercise_id = data.get('exercise_id')
    workout_id = data.get('workout_id')
    for i in return_load:
        create_load(i[0], i[1], exercise_id, workout_id)


    inline_keaboard = InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('Додати ще', callback_data='add')
    button2 = types.InlineKeyboardButton('Закінчити та повернутись до сторінки', callback_data='back')
    inline_keaboard.add(button1, button2)

    await message.answer('Що далі?', reply_markup=inline_keaboard)


@dp.callback_query_handler(lambda query: query.data == 'add', state='*')
async def add_exercise(callback_query: types.CallbackQuery, state: FSMContext):
    await AuthState.USER_WORKOUT_NAME.set()
    new_workout = False
    await state.update_data(new_workout=new_workout)
    await workout_name(callback_query.message, state)


@dp.callback_query_handler(lambda query: query.data == 'back', state='*')
async def back(callback_query: types.CallbackQuery, state: FSMContext):
    await AuthState.USER_ACCOUNT.set()
    await account(callback_query.message, state)
