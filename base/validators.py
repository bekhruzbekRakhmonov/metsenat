from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class UsernameValidator(validators.RegexValidator):
    regex = r"^[\w.@+-]+\Z"

    message = _(
        "Enter a valid username. This value may contain only letters, "
        "numbers, and @/./+/-/_ characters."
    )

    flags = 0

class PhoneNumberValidator(validators.RegexValidator):
    regex = r"\+(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|2[98654321]\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2[70]|7|1)\d{1,14}$"

    message = _(
        "Enter a valid phone number."
    )

    flags = 0

def payment_amount_validator(value):
    if value <= 0:
        raise ValidationError(_("Amount should be greater than 0."))
