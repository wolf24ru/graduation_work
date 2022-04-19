from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class PhoneNumberValidator(validators.RegexValidator):
    regex = r"(\+?7|8)?[\- ]?(\(?\d{3}\)?)?[\- ]?(\d{7}|\d[\-\d ]{5,7}\d)[ |\,]"
    message = _(
        "Enter a valid phone number. Format for phone number: "
        "+7 (XXX) XXX XX-XX"
        "+7XXXXXXXXXX"
        "8XXXXXXXXXX"
        "+7 (XXX)-XXX-XX-XX"
        "+7 XXX-XXX-XX-XX"
    )
    flags = 0
