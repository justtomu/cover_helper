from keyboards.callback_data import pagination_cb, action_cb
from text import t

from aiogram import types as ty


class PaginationKeyboard:
    @staticmethod
    def render_pagination_buttons(keyboard, page, total_pages, action, back_btn=None):
        if page != 1:
            keyboard.add(
                ty.InlineKeyboardButton(
                    text=f'⬅️{page - 1}',
                    callback_data=pagination_cb.new(action=action, data=str(page - 1))
                )
            )
            keyboard.insert(
                ty.InlineKeyboardButton(
                    text=f'{page}/{total_pages}',
                    callback_data=pagination_cb.new(action='q', data='q')
                )
            )
        else:
            keyboard.add(
                ty.InlineKeyboardButton(
                    text=f'{page}/{total_pages or 1}',
                    callback_data=pagination_cb.new(action='q', data='q')
                )
            )
        if page < total_pages:
            keyboard.insert(
                ty.InlineKeyboardButton(
                    text=f'➡️️{page + 1}',
                    callback_data=pagination_cb.new(action=action, data=str(page + 1))
                )
            )
        if not back_btn:
            keyboard.row(
                ty.InlineKeyboardButton(
                    t('main.back'),
                    callback_data=action_cb.new(action='to_main')
                )
            )
        else:
            keyboard.row(
                back_btn
            )
        return keyboard
