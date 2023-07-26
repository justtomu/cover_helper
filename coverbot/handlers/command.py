from keyboards import main
from text import t
from utils import start
from utils.states import Main

handlers = start.create_handlers_registry()


@handlers.register_message_handler(commands=['start'], state='*')
async def main_start(message, state):
    await Main.main_menu.set()
    await message.answer(t('main.welcome'), reply_markup=main())




