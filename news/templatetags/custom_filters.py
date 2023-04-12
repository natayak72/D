from django import template
import re

# регистрация фильтров
register = template.Library()

@register.filter(name='censor')
def censor(value):
    words = ['lorem', 'dolor', 'amet']

    for word in words:
        regexp = re.compile(re.escape(word), re.IGNORECASE)
        value = regexp.sub('', value)

    return value
