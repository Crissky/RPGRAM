import re


def escape_markdown_v2(text):
    for char in r'\_*[]()~`>#+-=|{}.!':
        text = text.replace(char, f'\{char}')
    return text


def escape_basic_markdown_v2(text):
    for char in r'_[](){}>#+-=|.!':
        text = text.replace(char, f'\{char}')
    return text


def remove_bold(text):
    return text.replace('*', '')


def remove_italic(text):
    return re.sub(r'_\b|\b_', '', text)


def remove_code(text):
    return text.replace('`', '')
