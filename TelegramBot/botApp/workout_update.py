# from aiogram import types
# from aiogram.dispatcher import FSMContext
# from aiogram.types import InlineKeyboardMarkup
#
# from .account_action import program_workouts
# from .app import dp
# from .states import *
# from .settings import urls
# from .functions import delete_workout
# from .fetch import get_simple_data
#
#
#
# @dp.callback_query_handler(lambda query: query.data == 'update_workout', state=AuthState.USER_ACCOUNT)
# async def workout_update(callback_query: types.CallbackQuery, state: FSMContext):
#     await AuthState.USER_UPDATE_WORKOUT.set()
#     await callback_query.message.answer('Уведіть назву тренування')
#
#
# @dp.message_handler(state=AuthState.USER_UPDATE_WORKOUT)
# async def workout_to_update(message: types.Message, state: FSMContext):
#     workout_name = message.text
#     data = await state.get_data()
#     program_id = data.get('program_id')
#
#     await AuthState.USER_ACCOUNT.set()
#     workout = await get_simple_data(urls['workout_by_name_program_id'], program_id, workout_name)
#     workout_id = workout['id']
#
#     inline_keaboard = InlineKeyboardMarkup()
#     button1 = types.InlineKeyboardButton('Додати вправу',callback_data='insert_workout')
#     button2 = types.InlineKeyboardButton('Видалити вправу', callback_data='delete_workout')
#     await message.answer('', state)