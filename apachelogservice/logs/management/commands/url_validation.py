from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.core.management.base import BaseCommand, CommandError



class GivenUrlValidator:
    """
    Класс ответственный за валидацию переданного параметра url
    """
    def __call__(self, passed_url: str) -> str:
        validator = URLValidator()
        try:
            validator(passed_url)
        except ValidationError as e:
            raise CommandError(f'Given URL is not valid, {e}')
        else:
            return passed_url
