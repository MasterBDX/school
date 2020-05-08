import re

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _, ngettext


class IsAsciiValidator(object):
    def validate(self, password, user=None):
        if not password.isascii():
            raise ValidationError(
                _(
                    # "The password must contain at least 1 uppercase letter, A-Z."
                    "يجب إستخدام حروف الأبجدية الإنجليزية فقط "
                ),
                code='password_no_upper',
            )

    def get_help_text(self):
        return _(
            # "Your password must contain at least 1 uppercase letter, A-Z."
            "يجب إستخدام حروف الأبجدية الإنجليزية فقط "
        )


class MinimumLengthValidator:
    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                ngettext(
                    "This password is too short. It must contain at least %(min_length)d character.",
                    "كلمة المرور هذه قصيرة جدًا. يجب أن تحتوي على %(min_length)d  أحرف على الأقل.",
                    # "This password is too short. It must contain at least %(min_length)d characters.",
                    self.min_length
                ),
                code='password_too_short',
                params={'min_length': self.min_length},
            )

    def get_help_text(self):
        return ngettext(
            "Your password must contain at least %(min_length)d character.",
            "يجب أن تحتوي كلمة المرور على %(min_length)d من الأحرف على الأقل.",
            #"Your password must contain at least %(min_length)d characters.",
            self.min_length
        ) % {'min_length': self.min_length}


class NumberValidator(object):
    def validate(self, password, user=None):
        if not re.findall('\d', password):
            raise ValidationError(
                # "The password must contain at least 1 digit, 0-9.",
                _("يجب أن تحتوي كلمة المرور على رقم واحد على الأقل ، 0-9."),
                code='password_no_number',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 digit, 0-9."
        )


class NumberValidator(object):
    def validate(self, password, user=None):
        if not re.findall('\d', password):
            raise ValidationError(
                _(
                    # "The password must contain at least 1 digit, 0-9."
                    "يجب أن تحتوي كلمة المرور الخاصة بك على رقم واحد على الأقل ، 0-9."
                ),
                code='password_no_number',
            )

    def get_help_text(self):
        return _(
            # "Your password must contain at least 1 digit, 0-9."
            "يجب أن تحتوي كلمة المرور الخاصة بك على رقم واحد على الأقل ، 0-9."
        )


class UppercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                _(
                    # "The password must contain at least 1 uppercase letter, A-Z."
                    "يجب أن تحتوي كلمة المرور على حرف كبير واحد على الأقل ، A-Z."
                ),
                code='password_no_upper',
            )

    def get_help_text(self):
        return _(
            # "Your password must contain at least 1 uppercase letter, A-Z."
            "يجب أن تحتوي كلمة المرور على حرف واحد كبير على الأقل ، من A إلى Z."
        )


class LowercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[a-z]', password):
            raise ValidationError(
                _(
                    # "The password must contain at least 1 lowercase letter, a-z."
                    "يجب أن تحتوي كلمة المرور على حرف صغير واحد على الأقل ، a-z."
                ),
                code='password_no_lower',
            )

    def get_help_text(self):
        return _(
            # "Your password must contain at least 1 lowercase letter, a-z."
            "يجب أن تحتوي كلمة المرور على حرف صغير واحد على الأقل ، a-z."
        )


class SymbolValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
            raise ValidationError(
                _(
                    "يجب أن تحتوي كلمة المرور على رمز واحد على الأقل:" +
                    # "The password must contain at least 1 symbol: " +
                    "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"
                ),
                code='password_no_symbol',
            )

    def get_help_text(self):
        return _(
            "يجب أن تحتوي كلمة المرور على رمز واحد على الأقل:" +
            # "Your password must contain at least 1 symbol: " +
            "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"
        )
