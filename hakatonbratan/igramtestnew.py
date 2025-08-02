import asyncio
import logging
from aiogram import Bot, Dispatcher, types, Router
from aiogram import F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
import Admin, bdjso
logging.basicConfig(level=logging.INFO)
bot = Bot(token="8492891888:AAG71VfL8tnLBmu_1lsOji_JZmqkzwq8xOo")
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
    await message.reply("Отличный выбор!")

@dp.message(F.text.lower() == "помогите")
async def without_puree(message: types.Message,state:FSMContext):
    await message.reply("Подробно опишите вашу проблему, в ближайшее время с вами свяжется наш администратор")
    return await state.set_state(Message_to_group.help_input)

@dp.message(Message_to_group.help_input)
async def obrabotka_zaprosa(message: types.Message, state: FSMContext):
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
        await state.clear()
        messageforgroup = "\n".join(mass)
        await bot.send_message(-4681080381, messageforgroup + "\nИмя пользователя: @    " + message.from_user.username)

if __name__ == "__main__":
    asyncio.run(main())