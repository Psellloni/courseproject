import os
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from collections import defaultdict
from aiogram import types, F
from aiogram.filters import Command

from keyboards import start_keyboard, keyboard11
from utils import start_text, add_text

import os
import sys

sys.path.append(os.getcwd())

from connectors.db_connector.connector import add_user, validate_chat

# Get environment variables
# API_URL = os.getenv("API_URL")
# from source.config import telegram_api_key

# Initialize bot and dispatcher
bot = Bot(token="7899272807:AAGbH-MT53NpEcFs_1ABI5GzRehNJl3yGpU")
dp = Dispatcher()

# async def check_text(text: str) -> dict | None:
#     """Send text to API endpoint and return response"""
#     async with aiohttp.ClientSession() as session:
#         try:
#             async with session.post(
#                 API_URL,
#                 json={"text": text},
#                 timeout=aiohttp.ClientTimeout(total=3)
#             ) as response:
#                 if response.status == 200:
#                     return await response.json()
#         except (aiohttp.ClientError, asyncio.TimeoutError):
#             return None

@dp.message(CommandStart())
async def command_start_handler(message: types.Message):
    print()
    await message.answer(f"Hello, {message.from_user.full_name}!" + start_text, reply_markup=start_keyboard)

# @dp.message()
# async def reply(message: types.Message):
#     await message.reply('pupa')

@dp.message(Command("id"))
async def cmd_id(message: types.Message):
    chat_id = message.chat.id
    await message.reply(f"🆔 Chat ID: {chat_id}")

selected_options = {}
options = ["violnce", "terrorism", "racism", "politics"]

def generate_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """Generate keyboard with checkmarks for selected options"""
    buttons = []
    options = [
        ("Politics", "politics"),
        ("Racism", "racism"),
        ("Terrorism", "terrorism"),
        ("Violence", "violence")
    ]
    
    for text, data in options:
        if data in selected_options[user_id]['options']:
            text += " ✓"
        buttons.append(InlineKeyboardButton(text=text, callback_data=data))

    buttons.append(InlineKeyboardButton(text="Select →", callback_data="select"))
    keyboard = [buttons[i:i+2] for i in range(0, len(buttons), 2)]
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard, resize_keyboard=True)

@dp.callback_query(lambda c: c.data == "add")
async def process_add_callback(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Add a bot to your chat, give it admin rights. and send /id command. The bot will provide you with your chat id. Please send the Telegram chat id.")

@dp.message(F.text.regexp(r'^-(\d+)$'))
async def handle_telegram_links(message: types.Message):
    chat = message.text
    selected_options[message.from_user.id] = {}
    selected_options[message.from_user.id]["chat_id"] = chat
    selected_options[message.from_user.id]['options'] = set()

    await message.answer(
            f"Chat ID {chat} registered. Select categories to moderate:",
            reply_markup=generate_keyboard(message.from_user.id)
        )
    
@dp.message()
async def handle_telegram_links(message: types.Message):
    await message.reply("This message contain violence. @pselloni")

@dp.callback_query(lambda c: c.data in {"politics", "racism", "terrorism", "violence"})
async def process_option_callback(callback_query: types.CallbackQuery):
    """Toggle selection for individual options"""
    user_id = callback_query.from_user.id
    option = callback_query.data

    if option in selected_options[user_id]['options']:
        selected_options[user_id]['options'].discard(option)
    else:
        selected_options[user_id]['options'].add(option)

    await callback_query.message.edit_reply_markup(
        reply_markup=generate_keyboard(user_id)
    )

@dp.callback_query(lambda c: c.data == "select")
async def process_select_callback(callback_query: types.CallbackQuery):
    """Final selection handler"""
    user_id = callback_query.from_user.id
    selections = selected_options[user_id]['options']

    for op in options:
        selected_options[user_id][op] = (op in selected_options[user_id]['options'])
    
    if not selections:
        await callback_query.answer("Please select at least one option!")
        return
    
    if validate_chat(str(user_id), selected_options[user_id]['chat_id']):
        await callback_query.answer("Admin for this chat already exist!")
        return
    
    add_user(
        str(user_id), 
        selected_options[user_id]['chat_id'], 
        selected_options[user_id]['violnce'], 
        selected_options[user_id]['terrorism'], 
        selected_options[user_id]['racism'], 
        selected_options[user_id]['politics'], 
        )

    selected_options[user_id].clear()
    await callback_query.message.delete()
    await callback_query.message.answer(f"Saved {len(selections)} categories!")

async def main():
    await dp.start_polling(bot)

import asyncio
asyncio.run(main())