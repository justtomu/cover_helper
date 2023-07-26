from aiogram.utils.callback_data import CallbackData

action_cb = CallbackData('main', 'action')
edit_cb = CallbackData('edit', 'action')
pagination_cb = CallbackData('pagination', 'action', 'data')
history_cb = CallbackData('history', 'action', 'data')
