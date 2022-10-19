from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from os import getenv

load_dotenv()
API_TOKEN = getenv("API_TOKEN")
ADMIN_ID = getenv("ADMIN_ID")


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

