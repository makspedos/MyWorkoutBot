from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup
from .app import dp
from .states import *
from .fetch import *
from .functions import create_load, create_workout,update_exercise
from .settings import urls



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


    muscles = await get_simple_data(urls['muscle_all'])

    inline_keaboard = InlineKeyboardMarkup()
    buttons = [types.InlineKeyboardButton(muscle['name'], callback_data =f'muscle_{muscle["id"]}') for muscle in muscles]
    inline_keaboard.add(*buttons)
    await message.answer('Обери м`яз,на яку буде вправа', reply_markup=inline_keaboard)


@dp.callback_query_handler(lambda query: query.data.startswith('muscle_'), state=AuthState.USER_CHOOSE_MUSCLE)
async def muscle_select(callback_query: types.CallbackQuery, state: FSMContext):
    muscle_id = callback_query.data.split('_')[1]
    exercises = await get_simple_data(urls['exercise_by_muscle_id'],muscle_id)
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
    workout = await get_simple_data(urls['workout_by_program_id'], program_id)
    workout_id = workout[-1]['id']

    print('workout_id' + str(workout_id) + '\t' + str(exercise_id))
    await state.update_data(workout_id=workout_id)

    update_exercise(exercise_id, workout_id)
    await state.update_data(exercise_id=exercise_id)
    await AuthState.USER_ENTER_LOAD.set()
    await callback_query.message.answer('Уведи вагу та кількість повторів як: 115/8, 100/2 ...')


@dp.message_handler(state=AuthState.USER_ENTER_LOAD)
async def load_process(message: types.Message, state: FSMContext):
    loads = message.text
    loads = loads.split(', ')
    return_load = [load.split('/') for load in loads]

    data = await state.get_data()
    exercise_id = data.get('exercise_id')
    workout_id = data.get('workout_id')
    program_id = data.get('program_id')
    for i in return_load:
        create_load(i[0], i[1], exercise_id, workout_id, program_id)

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
