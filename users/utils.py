import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.conf import settings
from .models import PasswordHistory
from django.contrib.auth.hashers import check_password

class PasswordValidator:
    def validate(self, password, user=None):
        if len(password) < settings.PASSWORD_CONFIG.get('MIN_LENGTH', 10):
            raise ValidationError(
                _("Password must be at least 10 characters."),
                code='password_too_short'
            )

        if not any(char.isupper() for char in password):
            if settings.PASSWORD_CONFIG.get('UPPERCASE', True):
                raise ValidationError(
                    _("Password must contain at least one uppercase letter."),
                    code='password_no_uppercase'
                )
        if not any(char.islower() for char in password):
            if settings.PASSWORD_CONFIG.get('LOWERCASE', True):
                raise ValidationError(
                    _("Password must contain at least one lowercase letter."),
                    code='password_no_lowercase'
                )
        if not any(char.isdigit() for char in password):
            if settings.PASSWORD_CONFIG.get('DIGITS', True):
                raise ValidationError(
                    _("Password must contain at least one digit."),
                    code='password_no_digit'
                )
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            if settings.PASSWORD_CONFIG.get('SPECIAL_CHARS', True):
                raise ValidationError(
                    _("Password must contain at least one special character."),
                    code='password_no_special_character'
                )
        try:
            password_history = PasswordHistory.objects.filter(user=user)
        except Exception as e:
            print(e)
            return
        last_password_history = [pwd for pwd in password_history][:settings.PASSWORD_CONFIG.get('HISTORY_LIMIT')]
        for pwd in last_password_history:
            if check_password(password, pwd.password_hash):
                raise ValidationError(
                    _("Password already been used before."),
                    code='password_already_used'
                )

    def get_help_text(self):
        return None