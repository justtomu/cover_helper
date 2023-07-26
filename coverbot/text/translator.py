
class Translator:
    def __init__(self):
        self._translations = None

    def __call__(self, text_ids, language='ru'):
        parts = text_ids.split('.')
        node = self._translations
        for part in parts:
            node = node[part]

        return node[language]

    def translations(self, text_id):
        return self._translations[text_id]

    def load_translations(self, translation_id):
        assert translation_id in ['cover_bot']

        def load_trading_bot():
            from .cover_bot import translations
            return translations

        if translation_id == 'cover_bot':
            translations = load_trading_bot()
            self._set_translations(translations)

    def branch_translator(self, branch):
        t = Translator()
        t._set_translations(self._translations[branch])

        return t

    def _set_translations(self, translations):
        self._translations = translations
