import re

from rest_framework import serializers


class LinkValidator:
    """ Валидатор """
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        """ Проверяет, что ссылка соответствует требованию: 'youtube.com' """
        # Регулярное выражение для поиска ссылок
        youtube_pattern = re.compile(r'^(https?://)?(www\.)?youtube\.com/?$')
        link_to_video = dict(value).get(self.field)

        if link_to_video is None:
            return ''

            # Проверка на наличие запрещённых ссылок
        if not bool(youtube_pattern.match(link_to_video)):
            raise serializers.ValidationError("Сторонняя ссылка. Не соответствует требованиям.")

# other_links_pattern = r'https?://[^\s/]+(?:\.[^\s/]+)+[^\s]*'
