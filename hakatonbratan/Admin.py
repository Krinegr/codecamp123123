from aiogram import types, Router
from aiogram import F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
import json
router = Router()

class Helper(StatesGroup):
    Helper_input= State()
    Delete_input=State()
@router.message(Command("admin"))
async def Is_user_admin(message: types.Message, state:FSMContext):
    Hello_admin = "Здравствуйте администратор, чтобы войти в режим удаления напишите /deleter"
    if message.from_user.id == 1427364974:
        kb = [
            [
                types.KeyboardButton(text="Просмотреть запросы"),
            ],
        ]
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True,
            input_field_placeholder="Поддержка компании ООО _Тмыв бабла_"
        )
        await message.answer(Hello_admin, reply_markup=keyboard)
        return await state.set_state(Helper.Helper_input)

    else:
        await message.answer("Вы не администратор")
        return None

@router.message(Command("deleter"))
async def IsUseradm(message: types.Message, state:FSMContext):
    Hello_admin = "Вы вошли в режим удаления запросов, чтобы удалить информацию напишите: 'delete: ' + 'айди запроса', чтобы выйти из этого режима, напишите dedeleter"
    if message.from_user.id == 1427364974:
        await message.answer(Hello_admin)
        return await state.set_state(Helper.Delete_input)
    return None
@router.message(F.text.lower() == "просмотреть запросы")
async def with_puree(message: types.Message):
    if message.from_user.id == 1427364974:
        with open("bdbd.json", 'r') as file:
            data = json.load(file)

        ids = [item["ID"] for item in data]
        max_id = max(ids) if ids else 0

        kb = [
            [

            ]
        ]
        for i in ids:
            kb[0].append(types.KeyboardButton(text=str(i)))
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True,
            input_field_placeholder="Поддержка компании ООО _Тмыв бабла_"
        )
        await message.answer("Все запросы в кнопках", reply_markup=keyboard)
    else:
        await message.answer("Вы не администратор")


@router.message(F.text,Helper.Helper_input)
async def handle_id_button(message: types.Message, state:FSMContext):
        input_id = message.text
        if input_id == "/deadmin":
            await message.answer("Выход из режима администратора, чтобы вернуться, напишите /admin", reply_markup=types.ReplyKeyboardRemove())
            await state.clear()
            return
        print(str(input_id))
        input_id = int(input_id)
        with open("bdbd.json", 'r') as file:
            data = json.load(file)
        item = next((item for item in data if item["ID"] == input_id), None)
        if item:
            response_text = item.get("text")
            username = item.get("name")
            await message.answer(f"Имя: {"@" + username}\nТекст: {response_text} , чтобы выйти из режима администратора напишите /deadmin")
        else:
            await message.answer("Запись не найдена.")


@router.message(F.text, Helper.Delete_input)
async def delete_record(message: types.Message, state: FSMContext):
    text = message.text.strip()  # Убираем лишние пробелы
    if text.startswith("delete:"):
        try:
            Id_To_Delete = int(text.split(":")[1].strip()) - 1  # Индексация с 0
            with open("bdbd.json", "r") as file:
                data = json.load(file)
            if Id_To_Delete < 0 or Id_To_Delete >= len(data):
                await message.answer("Неверный ID для удаления.")
                return
            data.pop(Id_To_Delete)
            with open('bdbd.json', 'w') as file:
                json.dump(data, file, indent=4)
            await message.answer(f"Запись с ID {Id_To_Delete + 1} успешно удалена. Чтобы вернуться в режим удаления напишите /deleter")
            await state.clear()
        except (IndexError, ValueError):
            await message.answer("Неверный формат команды. Используйте 'delete: <айди записи>'.")
    elif text.lower() == 'dedeleter':
        await state.clear()
        await message.answer('Вы вышли из режима удаления, чтобы вернуться, напишите /deleter')
    else:
        await message.answer("Пожалуйста, используйте команду в формате 'delete: <айди записи>'.")
