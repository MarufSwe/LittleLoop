from django import template
from django.utils.translation import get_language

register = template.Library()

# English to Bangla digit mapping
BANGLA_DIGITS = {
    '0': '০',
    '1': '১',
    '2': '২',
    '3': '৩',
    '4': '৪',
    '5': '৫',
    '6': '৬',
    '7': '৭',
    '8': '৮',
    '9': '৯',
}


@register.filter(name='bangla_number')
def bangla_number(value):
    """
    Convert English digits to Bangla digits if current language is Bangla.
    Usage: {{ phone_number|bangla_number }}
    """
    if not value:
        return value
    
    # Only convert if current language is Bangla
    if get_language() != 'bn':
        return value
    
    # Convert value to string
    value_str = str(value)
    
    # Replace each English digit with Bangla digit
    for eng_digit, bn_digit in BANGLA_DIGITS.items():
        value_str = value_str.replace(eng_digit, bn_digit)
    
    return value_str


@register.filter(name='default_trans')
def default_trans(value, default_value):
    """
    Return default value if value is empty, but translate the default.
    Usage: {{ value|default_trans:"Not set" }}
    """
    from django.utils.translation import gettext as _
    
    if value:
        return value
    return _(default_value)
