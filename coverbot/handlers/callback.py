from bard.api import get_cover_letter_text
from keyboards import back, main, settings, history, back_to_history
from keyboards.callback_data import action_cb, edit_cb, pagination_cb, history_cb
from renders.helpers import goto_section
from text import t
from utils import start
from utils.states import Main, Settings

handlers = start.create_handlers_registry()


@handlers.register_callback_query_handler(action_cb.filter(action='settings'), state=Main.main_menu)
async def settings_main(query, callback_data, state):
    await goto_section(
        query,
        t('settings.main'),
        settings()
    )
    await Main.settings.set()


@handlers.register_callback_query_handler(action_cb.filter(action='history'), state=Main.main_menu)
async def history_main(query, callback_data, state):
    async with state.proxy() as data:
        data['history_page'] = 1
        history_list = data.get('history', [])
    await goto_section(
        query,
        t('history.main'),
        history(history_list)
    )
    # await Main.history.set()


@handlers.register_callback_query_handler(action_cb.filter(action='to_main'), state='*')
async def back_to_main(query, callback_data, state):
    await goto_section(
        query,
        t('main.welcome'),
        main()
    )
    await Main.main_menu.set()


@handlers.register_callback_query_handler(action_cb.filter(action='skip'), state=Main.main_menu)
async def skip_user_data(query, callback_data, state):
    async with state.proxy() as data:
        data['skip_user_data'] = True
        vacancy_details = data['history'][-1]
    await query.message.answer(t('main.loading'))
    await query.message.answer(
        await get_cover_letter_text(vacancy_details, {})
    )


@handlers.register_callback_query_handler(edit_cb.filter(), state=Main.settings)
async def edit_user_data(query, callback_data, state):
    async with state.proxy() as data:
        data['setting_to_edit'] = callback_data['action']
    await query.message.answer(
        t('settings.enter_new_setting').format(
            t(f"settings.{callback_data['action']}")
        )
    )
    await state.set_state(f"Settings:enter_{callback_data['action']}")


@handlers.register_callback_query_handler(pagination_cb.filter(action='history'), state='*')
async def pagination_mailing(query, callback_data, state):
    page = int(callback_data.get('data', 0)) or 1
    text = t('history.main')
    async with state.proxy() as data:
        data['history_page'] = page
        history_list = data.get('history', [])
    keyboard = history(history_list, int(page))
    await goto_section(query, text, keyboard)


@handlers.register_callback_query_handler(history_cb.filter(action='info'), state='*')
async def pagination_mailing(query, callback_data, state):
    request_id = int(callback_data.get('data', 0))
    async with state.proxy() as data:
        history_el = data.get('history', [])[request_id]
        page = data.get('history_page', 1)
    text = t('history.info').format(
        company=history_el['company'],
        role=history_el['role'],
        text=history_el['text'],
        id=request_id
    )
    keyboard = back_to_history(page)
    await goto_section(query, text, keyboard)


