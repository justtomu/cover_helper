import functools
import logging

log_format = '[%(asctime)s] %(name)s - %(levelname)s - %(message)s'


logging.basicConfig(
    # filename='../logs.log',
    level=logging.INFO,
    format=log_format)

log = logging.getLogger()


async def render_state(state):
    state_name = await state.get_state()
    state_data = await state.get_data()
    return f'state={state_name}, data={state_data}'


def query_log_info(statement):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(query, callback_data, state):
            log.info(f'{statement} {func.__name__} callback_data: {callback_data} {await render_state(state)}')
            return await func(query, callback_data, state)
        return wrapper
    return decorator


def message_log_info():
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(message, state):
            log.info(f'{func.__name__} {await render_state(state)}')
            return await func(message, state)
        return wrapper
    return decorator

