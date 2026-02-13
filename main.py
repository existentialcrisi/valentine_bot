import asyncio
import logging
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# ===== НАСТРОЙКИ =====
BOT_TOKEN = "8534635189:AAFlkCu-RuCFMXDiepEsC2AkFhu79brheaQ"  # СЮДА ВСТАВЬТЕ СВОЙ ТОКЕН
ADMIN_ID = 873533454  # СЮДА ВСТАВЬТЕ СВОЙ ID (число)
# =====================

# Включаем логирование (чтобы видеть ошибки)
logging.basicConfig(level=logging.INFO)

# Создаём объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ===== БАЗА ВАЛЕНТИНОК (ДЛЯ КОМАНДЫ /valentine) =====
valentines = [
    "Ты как Wi-Fi — не вижу, но чувствую, что рядом ❤️",
    "С тобой даже понедельник похож на пятницу 🎉",
    "Если бы любовь была болезнью, я бы просил не лечить меня 💘",
    "Я влюбился в тебя, как программист в понятную документацию 🧡",
    "Ты — мой Ctrl+S, без тебя всё теряется 💾",
    "Спасибо, что ты есть! С 14 февраля 🌹",
]

# ===== КОМАНДА /start =====
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user = message.from_user
    # Приветствуем пользователя по имени
    await message.answer(
        f"Привет, {user.first_name}! 💌\n"
        "Я бот-валентинка. Отправь /valentine, и я пришлю тебе тёплые слова.\n"
        
    )
    # Уведомляем админа о новом пользователе
    await bot.send_message(
        ADMIN_ID,
        f"🆕 Новый пользователь:\n"
        f"ID: {user.id}\n"
        f"Имя: {user.full_name}\n"
        f"Username: @{user.username}" if user.username else "Username: не указан"
    )

# ===== КОМАНДА /valentine =====
@dp.message(Command("valentine"))
async def cmd_valentine(message: types.Message):
    text = random.choice(valentines)
    await message.answer(text)

# ===== ОБРАБОТКА ВСЕХ СООБЩЕНИЙ (НЕ КОМАНД) =====
@dp.message()
async def forward_to_admin(message: types.Message):
    # 1. Пересылаем сообщение админу (полная информация об отправителе)
    await message.forward(ADMIN_ID)

    # 2. Отправляем админу детальную информацию в текстовом виде
    user = message.from_user
    info = (
        f"📩 Сообщение от @{user.username}\n" if user.username else "📩 Сообщение от пользователя\n"
        f"ID: {user.id}\n"
        f"Имя: {user.full_name}\n"
        f"Текст: {message.text or '[медиа]'}\n"
        f"Время: {message.date}"
    )
    await bot.send_message(ADMIN_ID, info)

# ===== ЗАПУСК БОТА =====
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
