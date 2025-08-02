import asyncio
import logging
from aiogram import Bot, Dispatcher, types, Router
from aiogram import F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
router = Router()
@router.message(Command("admin"))
async def Is_user_admin(message: types.Message):
    Hello_admin = "Здравствуйте администратор"
    if message.from_user.id == 1427364974:
        await message.answer(Hello_admin)
        await message.answer(data)
    else:
        await message.answer("Вы не администратор")