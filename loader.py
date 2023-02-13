from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = getenv("API_TOKEN")
SBER_TOKEN = getenv("SBER_TOKEN")

ADMIN_ID = getenv("ADMIN_ID")
ABRAM_ID = getenv("ABRAM_ID")
DASHA_ID = getenv("DASHA_ID")
KIRILL_ID = getenv("KIRILL_ID")

storage = MemoryStorage()

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)
