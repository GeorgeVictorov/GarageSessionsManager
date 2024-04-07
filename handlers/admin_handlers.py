from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message, BufferedInputFile
from keyboards.keyboards import generate_admin_sessions, generate_admin_unpaid_sessions
from lexicon.lexicon import MESSAGES, INFO
from database.db_admin import admin_upcoming_sessions, admin_cancel_session, admin_canceled_info, \
    admin_confirm_session_payment, update_types_price, admin_ban_or_unban_user
from database.select_data import get_sessions_history, history_to_csv, generate_filename, get_type_prices, \
    get_users
from database.sqlite import update_cached_users
from database.db_admin import clear_cache
from services.admin import format_sessions
from filters.admin import IsAdmin
from filters.callback_factory import AdminCancelCallback, AdminPaymentCallback
from config_data.config import load_config
from config_data.commands import ADMIN_COMMANDS
from middlewares.registration_middleware import RegistrationMiddleware

router = Router()
router.message.middleware(RegistrationMiddleware())


@router.message(IsAdmin(), Command(commands=ADMIN_COMMANDS))
async def admin_commands_handler(message: Message):
    command = message.text.split()[0]

    if command == '/admin':
        username = message.from_user.username
        await message.answer(MESSAGES['/admin'].format(username), parse_mode='HTML')

    elif command == '/admin_upcoming':
        booked_sessions = admin_upcoming_sessions()
        response_message = format_sessions(booked_sessions)
        await message.answer(response_message, parse_mode='HTML')

    elif command == '/admin_cancel':
        keyboard_markup = generate_admin_sessions()

        if keyboard_markup.inline_keyboard:
            response_message = MESSAGES['/admin_cancel']
        else:
            response_message = MESSAGES['/admin_no_upcoming']

        await message.answer(response_message, parse_mode='HTML', reply_markup=keyboard_markup)

    elif command == '/admin_payment':
        keyboard_markup = generate_admin_unpaid_sessions()

        if keyboard_markup.inline_keyboard:
            response_message = MESSAGES['/admin_payment']
        else:
            response_message = MESSAGES['/admin_no_payment']

        await message.answer(response_message, parse_mode='HTML', reply_markup=keyboard_markup)

    elif command == '/admin_sessions':
        cols, rows = get_sessions_history()
        if cols:
            csv_data = history_to_csv(cols, rows)
            file_name = generate_filename(rows)
            await message.answer(text=MESSAGES['/admin_sessions'], parse_mode='HTML')
            await message.answer_document(BufferedInputFile(csv_data.encode(), filename=file_name))

    elif command == '/admin_price':
        type_prices = get_type_prices()
        if type_prices:
            price_message = "<b>Type Prices:</b>\n\n"
            for type_desc, price in type_prices:
                price_message += f"{type_desc}: {price}\n"
            await message.answer(price_message, parse_mode='HTML')

    elif command == '/admin_users':
        users = get_users()
        if users:
            user_message = "<b>Users:</b>\n\n"
            for user_id, username, phone, ban in users:
                user_message += f"<b>{username}</b> | ID: <b>{user_id}</b>\n"
                user_message += f"{phone} | {ban}\n\n"
            await message.answer(user_message, parse_mode='HTML')

    elif command == '/update_price':
        command_args = message.text.split()

        if len(command_args) != 3:
            await message.answer(MESSAGES['/admin_update_price'], parse_mode='HTML')
            return

        _, type_id, new_price = message.text.split()
        type_desc = update_types_price(type_id, new_price)
        if type_desc is not None:
            await message.answer(f"Price for type: <b>{type_desc}</b> updated to <b>{new_price}</b>.",
                                 parse_mode='HTML')
        else:
            await message.answer("An error occurred while updating price. Please try again later.")

    elif command == '/ban_user':
        command_args = message.text.split()

        if len(command_args) != 3:
            await message.answer(MESSAGES['/ban_user'], parse_mode='HTML')
            return

        _, user_id, status = message.text.split()
        user_id = int(user_id)
        if user_id not in load_config().tg_bot.admin_ids:
            status = admin_ban_or_unban_user(user_id, int(status))
            if status is not None:
                update_cached_users()
                clear_cache()
                await message.answer(f"Status for: <b>{user_id}</b> has been changed.", parse_mode='HTML')
            else:
                await message.answer("An error occurred while changing the status.")
        else:
            await message.answer("<b>Impossible to ban an admin.</b>", parse_mode='HTML')

    elif command == '/send_message':
        command_args = message.text.split(maxsplit=1)

        if len(command_args) != 2:
            await message.answer(MESSAGES['/send_message'], parse_mode='HTML')
            return

        text = command_args[1]

        users = get_users()
        if users:
            for user_id, _, _, _ in users:
                await message.bot.send_message(user_id, text)
        await message.answer("Message sent to all users.")


@router.callback_query(F.data == 'admin_close', IsAdmin())
async def close_admin_cancel_upcoming_sessions(callback_query: CallbackQuery):
    await callback_query.message.edit_text(text=INFO['close'],
                                           parse_mode='HTML')


@router.callback_query(AdminCancelCallback.filter(), IsAdmin())
async def admin_cancel_upcoming_sessions(callback_query: CallbackQuery,
                                         callback_data: AdminCancelCallback):
    action, session_id = callback_data.pack().split('-')
    username = callback_query.from_user.username
    session_start, duration, type_desc = admin_canceled_info(session_id)

    admin_cancel_session(int(session_id))

    keyboard_markup = generate_admin_sessions()

    for admin_id in load_config().tg_bot.admin_ids:
        admin_message = INFO['session_admin_cancel'].format(username, session_start, duration, type_desc)
        await callback_query.bot.send_message(admin_id, admin_message, parse_mode='HTML')

    if keyboard_markup.inline_keyboard:
        response_message = MESSAGES['/admin_cancel']
    else:
        response_message = MESSAGES['/admin_no_upcoming']

    await callback_query.message.edit_text(response_message, parse_mode='HTML', reply_markup=keyboard_markup)


@router.callback_query(AdminPaymentCallback.filter(), IsAdmin())
async def admin_confirm_payment(callback_query: CallbackQuery,
                                callback_data: AdminPaymentCallback):
    action, session_id = callback_data.pack().split('-')
    username = callback_query.from_user.username
    session_start, duration, type_desc = admin_canceled_info(session_id)

    admin_confirm_session_payment(int(session_id))

    keyboard_markup = generate_admin_unpaid_sessions()

    for admin_id in load_config().tg_bot.admin_ids:
        admin_message = INFO['session_admin_payment'].format(username, session_start, duration, type_desc)
        await callback_query.bot.send_message(admin_id, admin_message, parse_mode='HTML')

    if keyboard_markup.inline_keyboard:
        response_message = MESSAGES['/admin_payment']
    else:
        response_message = MESSAGES['/admin_no_payment']

    await callback_query.message.edit_text(response_message, parse_mode='HTML', reply_markup=keyboard_markup)

#
# @router.message(Command(commands='admin'), IsAdmin())
# async def admin_start(message: Message):
#     username = message.from_user.username
#     await message.answer(MESSAGES['/admin'].format(username), parse_mode='HTML')
#
#
# @router.message(Command(commands='admin_upcoming'), IsAdmin())
# async def admin_upcoming(message: Message):
#     booked_sessions = admin_upcoming_sessions()
#     response_message = format_sessions(booked_sessions)
#     await message.answer(response_message, parse_mode='HTML')
#
#
# @router.message(Command(commands='admin_cancel'), IsAdmin())
# async def admin_cancel(message: Message):
#     keyboard_markup = generate_admin_sessions()
#
#     if keyboard_markup.inline_keyboard:
#         response_message = MESSAGES['/admin_cancel']
#     else:
#         response_message = MESSAGES['/admin_no_upcoming']
#
#     await message.answer(response_message, parse_mode='HTML', reply_markup=keyboard_markup)
#
#
# @router.callback_query(F.data == 'admin_close', IsAdmin())
# async def close_admin_cancel_upcoming_sessions(callback_query: CallbackQuery):
#     await callback_query.message.edit_text(text=INFO['close'],
#                                            parse_mode='HTML')
#
#
# @router.message(Command(commands='admin_payment'), IsAdmin())
# async def admin_payment(message: Message):
#     keyboard_markup = generate_admin_unpaid_sessions()
#
#     if keyboard_markup.inline_keyboard:
#         response_message = MESSAGES['/admin_payment']
#     else:
#         response_message = MESSAGES['/admin_no_payment']
#
#     await message.answer(response_message, parse_mode='HTML', reply_markup=keyboard_markup)
#
#
# @router.message(Command(commands='admin_sessions'), IsAdmin())
# async def send_session_history(message: Message):
#     cols, rows = get_sessions_history()
#     if cols:
#         csv_data = history_to_csv(cols, rows)
#         file_name = generate_filename(rows)
#         await message.answer(text=MESSAGES['/admin_sessions'], parse_mode='HTML')
#         await message.answer_document(BufferedInputFile(csv_data.encode(), filename=file_name))
#
#
# @router.message(Command(commands='admin_price'), IsAdmin())
# async def send_type_prices(message: Message):
#     type_prices = get_type_prices()
#     if type_prices:
#         price_message = "<b>Type Prices:</b>\n\n"
#         for type_desc, price in type_prices:
#             price_message += f"{type_desc}: {price}\n"
#         await message.answer(price_message, parse_mode='HTML')
#
#
# @router.message(Command(commands='admin_users'), IsAdmin())
# async def send_user_list(message: Message):
#     users = get_users()
#     if users:
#         user_message = "<b>Users:</b>\n\n"
#         for user_id, username, phone, ban in users:
#             user_message += f"<b>{username}</b> | ID: <b>{user_id}</b>\n"
#             user_message += f"{phone} | {ban}\n\n"
#         await message.answer(user_message, parse_mode='HTML')
#
#
# @router.message(Command('admin_update_price'), IsAdmin())
# async def update_price(message: Message):
#     await message.answer(MESSAGES['/admin_update_price'], parse_mode='HTML')
#
#
# @router.message(Command(commands='update_price'), IsAdmin())
# async def confirm_update_price(message: Message):
#     command_args = message.text.split()
#
#     if len(command_args) != 3:
#         await message.answer(MESSAGES['/admin_update_price_error'])
#         return
#
#     _, type_id, new_price = message.text.split()
#     type_desc = update_types_price(type_id, new_price)
#     if type_desc is not None:
#         await message.answer(f"Price for type: <b>{type_desc}</b> updated to <b>{new_price}</b>.", parse_mode='HTML')
#     else:
#         await message.answer("An error occurred while updating price. Please try again later.")
#
#
# @router.message(Command('ban_user'), IsAdmin())
# async def ban_user(message: Message):
#     await message.answer(MESSAGES['/ban_user'], parse_mode='HTML')
#
#
# @router.message(Command(commands='ban'), IsAdmin())
# async def ban_or_unban(message: Message):
#     command_args = message.text.split()
#
#     if len(command_args) != 3:
#         await message.answer(MESSAGES['/ban_user_error'])
#         return
#
#     _, user_id, status = message.text.split()
#     user_id = int(user_id)
#     if user_id not in load_config().tg_bot.admin_ids:
#         status = admin_ban_or_unban_user(user_id, int(status))
#         if status is not None:
#             update_cached_users()
#             await message.answer(f"Status for: <b>{user_id}</b> has been changed.", parse_mode='HTML')
#         else:
#             await message.answer("An error occurred while changing the status.")
#     else:
#         await message.answer("Impossible to ban an admin.")
