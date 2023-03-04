from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram import types
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from services import get_faq, get_faq_children, get_faq_byId
from config import BOT_TOKEN
from bs4 import BeautifulSoup

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

faq_callback = CallbackData('faq', 'action' ,'id', 'text')

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    builder = InlineKeyboardMarkup()
    response = await get_faq()
    for i in response:
        hastext = "True" if i.get('text') else ""
        builder.add(types.InlineKeyboardButton(
            text=f"{i.get('title')}",
            callback_data = faq_callback.new(action='faqAct' ,id=int(i.get('id')), text=hastext))
            )
    await message.reply(
        'Дарова'
        , parse_mode=types.ParseMode.HTML, reply_markup=builder)


@dp.callback_query_handler(faq_callback.filter(action='faqAct'))
async def callbacks_num_change_fab(
        callback: types.CallbackQuery, 
        callback_data: dict
):
    if (callback_data['text']):
        response = await get_faq_byId(callback_data['id'])
        soap = BeautifulSoup(response.get("text"), 'html.parser')
        for i in soap.find_all("div"):
            if (i.img):
                src = i.img['src']
                i.img.decompose()
                await bot.send_photo(chat_id=callback.from_user.id, photo="https://play-lh.googleusercontent.com/6UgEjh8Xuts4nwdWzTnWH8QtLuHqRMUB7dp24JYVE2xcYzq4HA8hFfcAbU-R-PC_9uA1")
                text = i.encode_contents().decode()
                if text:
                    await callback.message.answer(text, parse_mode=types.ParseMode.HTML)
            else:
                await callback.message.answer(i.encode_contents().decode(), parse_mode=types.ParseMode.HTML)
            
        await callback.answer()

    else:
        builder = InlineKeyboardMarkup()
        id = callback_data['id']
        response = await get_faq_children(id)
        for i in response:
            hastext = "True" if i.get('text') else ""
            builder.add(types.InlineKeyboardButton(
                text=f"{i.get('title')}",
                callback_data=faq_callback.new(action='faqAct', id=int(i.get('id')), text=hastext)
                )
            )
        await callback.message.answer(
            "Выберите тот блок который соответствуе вашему запросу"
            , reply_markup=builder)
        await callback.answer()



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)