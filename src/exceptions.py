class ParserFindTagException(Exception):
    """Вызывается, когда парсер не может найти тег."""
    pass


class ParserFindStatusException(Exception):
    """Вызывается, когда статус в таблице и на странице не совпали."""
    pass
