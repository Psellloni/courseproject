from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


start_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[
    InlineKeyboardButton(text="add", callback_data="add"),
    InlineKeyboardButton(text="change", callback_data="change")
    ]], resize_keyboard=True)

keyboard11 = InlineKeyboardMarkup(
    inline_keyboard=[[
    InlineKeyboardButton(text="testing", callback_data="testing"),
    InlineKeyboardButton(text="микрочелики", callback_data="micro"),
    InlineKeyboardButton(text="MLаденцы", callback_data="cro")
    ]], resize_keyboard=True)

add_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[
    InlineKeyboardButton(text="Politics", callback_data="politics"),
    InlineKeyboardButton(text="Racism", callback_data="racism"),
    InlineKeyboardButton(text="Terrorism", callback_data="terrorism"),
    InlineKeyboardButton(text="Violence", callback_data="violence")
    ]], resize_keyboard=True)

keyboard0 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Политика", callback_data="politics"),
                                 InlineKeyboardButton(text="Мат", callback_data="swearing"),
                                 InlineKeyboardButton(text="СВО", callback_data="SVO")]
                                 ], resize_keyboard=True)

keyboard1 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Редактировать настройки текущих чатов", callback_data="edit"),
                                 InlineKeyboardButton(text="Добавить новый чат", callback_data="add")]
                                 ], resize_keyboard=True)