from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

class AccountActivationToken(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return text_type(user) + text_type(timestamp) + text_type(user.is_active)
    
password_reset_token = PasswordResetTokenGenerator()
account_activation_token = AccountActivationToken()