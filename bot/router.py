import bot.searcher
from random import choice
from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from bot.config import OWNER_ID
from bot.searcher import Searcher, search_image
from bot.utils import get_inline_keyboard


urt = Router()


search_queries = {
    "uraraka": ["Урарака Очако арт"],
    "izuocha": ["Uraraka x Midoriya"]
}
start_index = 0


@urt.message(Command('searcher'))
async def show_searcher(message: Message):
    await message.reply(f'{bot.searcher.current_searcher.value}\n`/set_searcher`',
                        parse_mode=ParseMode.MARKDOWN_V2)


@urt.message(Command("set_searcher"))
async def set_searcher(message: Message):
    if message.from_user.id != OWNER_ID:
        await message.reply('Запрещено / Forbidden!')
        return
    try:
        searcher_value = message.text.split()[1].lower()
        new_searcher = Searcher(searcher_value)
        bot.searcher.current_searcher = new_searcher
        await message.reply(f"Тип поиска обновлён на {new_searcher.value}.")
    except (IndexError, ValueError):
        await message.reply("Неверный тип поиска. Доступны: google, duckduckgo.")


@urt.message(Command("uraraka"))
async def send_uraraka(message: Message):
    query = choice(search_queries["uraraka"])
    image_url = await search_image(query, start_index)
    if image_url:
        await message.answer_photo(
            photo=image_url,
            reply_markup=get_inline_keyboard("uraraka")
        )
    else:
        await message.reply("Извините, не удалось найти изображение.")


@urt.message(Command("izuocha"))
async def send_izuocha(message: Message):
    query = choice(search_queries["izuocha"])
    image_url = await search_image(query, start_index)
    if image_url:
        await message.answer_photo(
            photo=image_url,
            reply_markup=get_inline_keyboard("izuocha")
        )
    else:
        await message.reply("Извините, не удалось найти изображение.")


@urt.callback_query(lambda callback_query: callback_query.data.startswith("new_picture:"))
async def new_picture_callback(callback_query: CallbackQuery):
    prefix = callback_query.data.split("new_picture:")[-1]
    query = choice(search_queries.get(prefix))
    if not query:
        await callback_query.answer("Неизвестный запрос.", show_alert=True)
        return
    image_url = await search_image(query, start_index)
    if image_url:
        await callback_query.message.answer_photo(
            photo=image_url,
            reply_markup=get_inline_keyboard(prefix)
        )
        await callback_query.answer()
    else:
        await callback_query.answer("Не удалось найти изображение.", show_alert=True)


@urt.message(Command('start_index'))
async def show_start_index(message: Message):
    global start_index
    await message.reply(f'{start_index}\n`/set_start_index`', parse_mode=ParseMode.MARKDOWN_V2)


@urt.message(Command('set_start_index'))
async def set_start_index(message: Message):
    if message.from_user.id != OWNER_ID:
        await message.reply('Запрещено / Forbidden!')
    else:
        global start_index
        try:
            start_index = int(message.text.split(' ')[1])
            await message.reply('Обновлено / Updated!')
        except Exception as _e:
            await message.reply('Нужно указывать число через пробел')


@urt.message(Command('start'))
async def start(message: Message):
    await message.answer(
        'Привет, я бот, отправляющий картинки с Очако Ураракой\n'
        'Hi, I\'m a bot that sends pictures of Ochaco Uraraka from My Hero Academia.\n\n'
        'Команды / Commands:\n'
        '/uraraka\n/izuocha\n/start_index\n/searcher'
    )
