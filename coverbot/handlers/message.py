from aiogram import types as ty

from bard.api import get_cover_letter_text
from keyboards import to_settings, settings
from renders.helpers import goto_section
from text import t
from utils import start
from utils.scrapper import get_vacancy_details
from utils.states import Main, Settings

handlers = start.create_handlers_registry()


@handlers.register_message_handler(content_types=['text'], state=Main.main_menu)
async def enter_vacancy(message: ty.message.Message, state):
    vacancy_type = 'url' if 'http' in message.text else 'text'

    vacancy_details = await get_vacancy_details(message.text) if vacancy_type == 'url' else {
        'text': message.text,
        'company': message.text[:10],
        'role': message.text[:10]
    }
    async with state.proxy() as data:
        skip_user_data = data.get('skip_user_data')
        user_data = data.get('user_data') or {}
        vacancy_details['id'] = str(len(data.get('history', [])))
        data['history'] = data.get('history', []) + [vacancy_details]
    if not user_data and not skip_user_data:
        await message.answer(t('main.user_details_error'), reply_markup=to_settings())
        return
    await message.answer(t('main.loading'))
    await message.answer(
        await get_cover_letter_text(vacancy_details, user_data)
    )


@handlers.register_message_handler(content_types=['text'], state=[
    Settings.enter_user_name,
    Settings.enter_years_of_experience,
    Settings.enter_last_position,
    Settings.enter_skills,
    Settings.enter_sphere_of_work,
])
async def edit_setting(message: ty.message.Message, state):
    setting_to_edit = str(await state.get_state()).split(':')[-1].replace('enter_', '')
    async with state.proxy() as data:
        data['user_data'] = {**data.get('user_data', {}), setting_to_edit: message.text.strip()}
    await message.answer(t('settings.setting_changed'))
    await goto_section(
        message,
        t('settings.main'),
        settings()
    )
    await Main.settings.set()
