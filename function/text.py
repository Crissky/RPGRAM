import re

from constant.text import SECTION_HEAD_ENEMY_START, SECTION_HEAD_ENEMY_END


def escape_markdown_v2(text: str):
    for char in r'\_*[]()~`>#+-=|{}.!':
        escaped_char = f'\{char}'
        text = text.replace(escaped_char, char)
        text = text.replace(char, escaped_char)

    return text


def escape_basic_markdown_v2(text: str):
    for char in r'_[](){}#+-=|.!':
        escaped_char = f'\{char}'
        text = text.replace(escaped_char, char)
        text = text.replace(char, escaped_char)

    return text


def remove_bold(text: str):
    return text.replace('*', '')


def remove_italic(text: str):
    return re.sub(r'_\b|\b_', '', text)


def remove_code(text: str):
    return text.replace('`', '')


def create_text_in_box(
    text: str,
    section_name: str,
    section_start: str = SECTION_HEAD_ENEMY_START,
    section_end: str = SECTION_HEAD_ENEMY_END,
    clean_func: callable = escape_basic_markdown_v2,
) -> str:
    text = text.strip()
    section_start = section_start.format(section_name)
    section_end = section_end.format(section_name)
    result = f'{section_start}\n\n{text}\n\n{section_end}'
    if callable(clean_func):
        result = clean_func(result)

    return result
