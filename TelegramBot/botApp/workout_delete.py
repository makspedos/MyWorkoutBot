from aiogram import types
from aiogram.dispatcher import FSMContext
from .account_action import program_workouts
from .app import dp
from .states import *

from .functions import delete_workout




@dp.callback_query_handler(lambda query: query.data == 'delete_workout', state=AuthState.USER_ACCOUNT)
async def workout_delete(callback_query: types.CallbackQuery, state: FSMContext):
    await AuthState.USER_DELETE_WORKOUT.set()
    await callback_query.message.answer('Уведіть назву тренування')


@dp.message_handler(state=AuthState.USER_DELETE_WORKOUT)
async def workout_to_delete(message: types.Message, state: FSMContext):
    workout_name = message.text
    await AuthState.USER_ACCOUNT.set()
    data = await state.get_data()
    program_id = data.get('program_id')
    user_id = data.get('user_id')
    delete_workout(workout_name, program_id)
    callback_data = f'program_{user_id}'
    callback_query = types.CallbackQuery(id='', from_user=message.from_user, chat=message.chat, message=message,
                                         data=callback_data)
    await program_workouts(callback_query, state)