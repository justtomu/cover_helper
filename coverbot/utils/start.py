
class HandlersRegistry:
    def __init__(self):
        self._handlers_registry = []

    def register_message_handler(self, *filters, commands=None, state=None, content_types=None):
        def decorator(callback):
            self._handlers_registry.append({
                'callback': callback,
                'filters': filters,
                'commands': commands,
                'state': state,
                'content_types': content_types,
                'type': 'message'
            })
            return callback

        return decorator

    def register_inline_handler(self, *filters, commands=None, state=None):
        def decorator(callback):
            self._handlers_registry.append({
                'callback': callback,
                'filters': filters,
                'commands': commands,
                'state': state,
                'type': 'query'
            })
            return callback

        return decorator

    def register_callback_query_handler(self, *filters, commands=None, state=None):
        def decorator(callback):
            self._handlers_registry.append({
                'callback': callback,
                'filters': filters,
                'commands': commands,
                'state': state,
                'type': 'callback'
            })
            return callback

        return decorator

    def apply_to_dispatcher(self, dispatcher):
        for handler in self._handlers_registry:
            if handler['type'] == 'message':
                dispatcher.register_message_handler(
                    handler['callback'],
                    *handler['filters'],
                    commands=handler['commands'],
                    state=handler['state'],
                    content_types=handler['content_types']
                )

            elif handler['type'] == 'callback':
                dispatcher.register_callback_query_handler(
                    handler['callback'],
                    *handler['filters'],
                    state=handler['state']
                )
            elif handler['type'] == 'query':
                dispatcher.register_inline_handler(
                    # handler['func'],
                    handler['callback'],
                    *handler['filters'],
                    state=handler['state']
                )
            else:
                assert False


def create_handlers_registry():
    return HandlersRegistry()

