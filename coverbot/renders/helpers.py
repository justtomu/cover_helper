from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import CantParseEntities, MessageCantBeEdited, InlineKeyboardExpected, BadRequest, \
    InvalidQueryID, MessageToDeleteNotFound
from aiogram import types as ty

from utils.log import log


async def goto_section(tg_object, text, keyboard=None, disable_preview=False, parse_mode='HTML', image=None):
    if isinstance(tg_object, CallbackQuery):
        # await tg_object.answer()
        tg_object.message.from_user = tg_object.from_user
        tg_object = tg_object.message
    try:
        photo_in_msg = tg_object.content_type == 'photo'
        if photo_in_msg and image:
            message = await tg_object.edit_media(
                media=ty.InputMedia(
                    type='photo', media=open(image, 'rb'), caption=text, parse_mode=parse_mode
                ),
                reply_markup=keyboard
            )
        elif photo_in_msg:
            message = await tg_object.edit_caption(caption=text, reply_markup=keyboard, parse_mode=parse_mode)
        elif not photo_in_msg and image:
            await tg_object.delete()
            message = await tg_object.answer_photo(caption=text, reply_markup=keyboard, parse_mode=parse_mode,
                                                   photo=open(image, 'rb'))
        else:
            message = await tg_object.edit_text(text=text, reply_markup=keyboard, parse_mode=parse_mode,
                                                disable_web_page_preview=disable_preview)
    except CantParseEntities as e:
        log.info('Error while send message: %s, message_text: %s', e, text)
        return await goto_section(tg_object=tg_object, text=text, keyboard=keyboard, disable_preview=disable_preview,
                                  parse_mode=None, image=image)
    except (MessageCantBeEdited, InlineKeyboardExpected, BadRequest, InvalidQueryID) as e:
        log.info('Error while edit message: %s', e)
        try:
            await tg_object.bot.delete_message(tg_object.from_user.id, tg_object.message_id)
        except MessageToDeleteNotFound:
            log.info(f'Error while delete message: {e}')
        if not image:
            message = await tg_object.answer(text=text, reply_markup=keyboard, parse_mode=parse_mode,
                                             disable_web_page_preview=disable_preview)
        else:
            message = await tg_object.answer_photo(caption=text, reply_markup=keyboard, parse_mode=parse_mode,
                                                   photo=open(image, 'rb'))
    return message
