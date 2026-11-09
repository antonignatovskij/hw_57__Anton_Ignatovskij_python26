from typing import Any, Callable, List

from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator

from django.utils.deconstruct import deconstructible



class AntonBaseValidator:
    @staticmethod
    def clean(x: str) -> List[str]:
        value = [v.strip().lower() for v in x.split()]
        return value


@deconstructible
class BanWordValidator(AntonBaseValidator):
    message = "В вашем поле присутствуют запрещенные слова: %(banned)s"
    code = "title_blacklist_words"

    def __init__(self, blacklist=None):
        if blacklist is None:
            blacklist = ['смерт', 'убийств', 'суицид', 'манья']
        if blacklist is not None:
            self.blacklist = blacklist
        self.banned = ''

    def __call__(self, value):
        cleaned = self.clean(value)
        if self.ban_contains(cleaned, self.blacklist):
            params = {"banned": self.banned}
            raise ValidationError(message=self.message, code=self.code, params=params)

    def ban_contains(self, words: List[str], blacklist: List[str]) -> bool:
        banlist = []
        for word in words:
            for banword in blacklist:
                if banword in word:
                    banlist.append(word)
                    break
        if len(banlist) == 0:
            return False
        else:
            self.banned = ', '.join(banlist)
            return True


@deconstructible
class IsItLinkValidator(AntonBaseValidator):
    message = "Ссылки запрещены!"
    code = "links_not_allowed"

    link_starts = ['http://', 'https://', 'www.']
    link_ends = ['.com', '.net', '.org', '.ru', '.kg', '.su', '.ai', '.tv']

    def __call__(self, value):
        cleaned = self.clean(value)
        if self.link_contains(cleaned):
            raise ValidationError(message=self.message, code=self.code)


    def link_contains(self, value):
        for v in value:
            for start in self.link_starts:
                for end in self.link_ends:
                    if v.startswith(start) and v.endswith(end):
                        return True
        return False

@deconstructible
class MinLengthValidator(BaseValidator):
    message = 'Ваша строка короче чем %(limit_value)s символов!'
    code = "min_value"

    def compare(self, a, b):
        return len(a) < b






