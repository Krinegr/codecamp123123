import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types, Router
from aiogram import F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
import json
import Admin
logging.basicConfig(level=logging.INFO)
bot = Bot(token="Token here")
dp = Dispatcher()
router = Router

async def main():
    dp.include_routers(Admin.router)
    await dp.start_polling(bot)

class Message_to_group(StatesGroup):
    help_input = State()
@dp.message(Command("start"))
async def cmd_start(message: types.Message,state:FSMContext):
    kb = [
        [
            types.KeyboardButton(text="FAQ"),
            types.KeyboardButton(text="Помогите")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Поддержка компании ООО _Тмыв бабла_"
    )
    await message.answer("Вы написали в поддержку компании ООО _Тмыв бабла_, выберите нужную вам опцию", reply_markup=keyboard)

@dp.message(F.text.lower() == "faq")
async def with_puree(message: types.Message):
    await message.reply("Если сайт не работает - перезагрузите ваш компьютер. Если FAQ оказалась недостаточной, просто напишите Помогите", reply_markup=types.ReplyKeyboardRemove())

@dp.message(F.text.lower() == "помогите")
async def without_puree(message: types.Message,state:FSMContext):
    await message.reply("Подробно опишите вашу проблему, укажите контакты, по которым можно с вами связаться и в ближайшее время с вами свяжется наш администратор", reply_markup=types.ReplyKeyboardRemove())
    global schet
    schet += 1
    return await state.set_state(Message_to_group.help_input)
schet = 0
@dp.message(Message_to_group.help_input)
async def obrabotka_zaprosa(message: types.Message, state: FSMContext ):
    text = message.text
    data = await state.get_data()
    if text != "Стоп":
        await message.reply(message.text)
        mass = data.get("message_saved", [])
        mass.append(text)
        await state.update_data(message_saved = mass)
    else:
        await message.reply("Отправлено")
        mass = data.get("message_saved")
        await message.reply("\n".join(mass))
        textfromuser = "\n".join(mass)
        username = message.from_user.username
        spisok = {
            "ID": schet,
            "text": textfromuser,
            "name": username
        }
        if os.path.exists("bdbd.json") and os.path.getsize("bdbd.json") > 0:
            with open("bdbd.json", 'r') as file:
                bata = json.load(file)
        else:
            bata = []
        bata.append(spisok)
        with open('bdbd.json', 'w') as file:
            json.dump(bata, file, indent=4)
        print(bata)
        print(schet)
        await state.clear()
        #messageforgroup = "\n".join(mass)
        await bot.send_message(-4681080381, "Отправили новый запрос о помощи, чтобы просмотреть его, откройте бота и напишите /admin    " + "\nИмя пользователя: @" + message.from_user.username)
        #await bot.send_message(-4681080381, messageforgroup + "\nИмя пользователя: @" + message.from_user.username)

if __name__ == "__main__":
    asyncio.run(main())
