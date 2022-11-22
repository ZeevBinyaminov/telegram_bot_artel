from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
from os import getenv

load_dotenv()
API_TOKEN = getenv("API_TOKEN")
ADMIN_ID = getenv("ADMIN_ID")
ABRAM_ID = getenv("ABRAM_ID")
DASHA_ID = getenv("DASHA_ID")

storage = MemoryStorage()

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)

