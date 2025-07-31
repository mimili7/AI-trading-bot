from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import config
import database
import payments

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    database.add_user(message.from_user.id)
    kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton("💳 Оплатить подписку", url=payments.create_invoice(message.from_user.id))
    )
    await message.answer("👋 Добро пожаловать! У тебя 1 час бесплатного доступа.\nПосле — нужна подписка.", reply_markup=kb)

@dp.message_handler(commands=["signals"])
async def signals(message: types.Message):
    if database.is_trial_active(message.from_user.id):
        await message.answer("📈 Торговый сигнал: Покупать BTC (пример)")
    else:
        kb = InlineKeyboardMarkup().add(
            InlineKeyboardButton("💳 Оплатить подписку", url=payments.create_invoice(message.from_user.id))
        )
        await message.answer("⛔ Пробный период закончился. Оплати подписку, чтобы продолжить.", reply_markup=kb)

def start_bot():
    executor.start_polling(dp)
