import logging

from requests import RequestException

from exceptions import ParserFindStatusException, ParserFindTagException


def get_response(session, url):
    try:
        response = session.get(url)
        response.encoding = 'utf-8'
        return response
    except RequestException:
        logging.exception(
            f'Возникла ошибка при загрузке страницы {url}',
            stack_info=True
        )


def find_tag(soup, tag, attrs=None):
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        error_msg = f'Не найден тег {tag} {attrs}'
        logging.error(error_msg, stack_info=True)
        raise ParserFindTagException(error_msg)
    return searched_tag


def error(text_name_status, dic,  link, td_tag):
    status_in_table = status_in_table = td_tag.text[1:]
    if text_name_status not in dic[status_in_table]:
        error_msg = f'''
        Несовпадающие статусы: {link}.
        Статус в карточке: {text_name_status}.
        Ожидаемые статусы: {dic[status_in_table]}
        '''
        logging.error(error_msg, stack_info=True)
        raise ParserFindStatusException(error_msg)
    return status_in_table
