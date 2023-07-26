import math

from aiogram import types as ty

from keyboards.callback_data import action_cb, edit_cb, history_cb, pagination_cb
from keyboards.pagination import PaginationKeyboard
from text import t


class MainKeyboard:
    def __call__(self, *args, **kwargs):
        keyboard = ty.InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            ty.InlineKeyboardButton(t('main.settings'), callback_data=action_cb.new(action='settings')),
            ty.InlineKeyboardButton(t('main.history'), callback_data=action_cb.new(action='history'))
        )
        return keyboard


class BackKeyboard:
    def __call__(self, *args, **kwargs):
        keyboard = ty.InlineKeyboardMarkup()
        keyboard.add(
            ty.InlineKeyboardButton(t('main.back'), callback_data=action_cb.new(action='to_main')),
        )
        return keyboard


class BackToHistory:
    def __call__(self, page=1):
        keyboard = ty.InlineKeyboardMarkup()
        keyboard.add(
            ty.InlineKeyboardButton(
                text=t('main.back'),
                callback_data=pagination_cb.new(action='history', data=str(page))
            )
        )
        return keyboard


class ToSettingsKeyboard:
    def __call__(self, *args, **kwargs):
        keyboard = ty.InlineKeyboardMarkup()
        keyboard.add(
            ty.InlineKeyboardButton(t('main.settings'), callback_data=action_cb.new(action='settings')),
            ty.InlineKeyboardButton(t('main.skip'), callback_data=action_cb.new(action='skip')),
        )
        return keyboard


class SettingsKeyboard:
    def __call__(self, *args, **kwargs):
        keyboard = ty.InlineKeyboardMarkup(row_width=1)
        keyboard.add(
            ty.InlineKeyboardButton(
                t('settings.user_name'),
                callback_data=edit_cb.new(action='user_name')
            ),
            ty.InlineKeyboardButton(
                t('settings.years_of_experience'),
                callback_data=edit_cb.new(action='years_of_experience')
            ),
            ty.InlineKeyboardButton(
                t('settings.last_position'),
                callback_data=edit_cb.new(action='last_position')
            ),
            ty.InlineKeyboardButton(
                t('settings.skills'),
                callback_data=edit_cb.new(action='skills')
            ),
            ty.InlineKeyboardButton(
                t('settings.sphere_of_work'),
                callback_data=edit_cb.new(action='sphere_of_work')
            ),
            ty.InlineKeyboardButton(
                t('main.back'),
                callback_data=action_cb.new(action='to_main')
            ),
        )
        return keyboard


class HistoryKeyboard:
    def __call__(self, history, page=1):
        keyboard = ty.InlineKeyboardMarkup(row_width=3)
        page_limit = 5
        total_pages = math.ceil(len(history) / page_limit)
        pag_start = (page - 1) * page_limit
        pag_end = pag_start + page_limit
        history_range = history[pag_start:pag_end]
        for history_el in history_range:
            keyboard.row(
                ty.InlineKeyboardButton(
                    text=history_el['company'][:10],
                    callback_data=history_cb.new(
                        action='info', data=history_el.get('id')
                    )
                )
            )
        keyboard = PaginationKeyboard.render_pagination_buttons(keyboard, page, total_pages, 'history')
        return keyboard
