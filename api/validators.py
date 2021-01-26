import datetime as dt

from django.core.exceptions import ValidationError


def validate_year(year):
    current_year = dt.datetime.now().year
    if year > current_year:
        raise ValidationError('Год должен быть меньше или равен текущему',
                              params={'год': year})
