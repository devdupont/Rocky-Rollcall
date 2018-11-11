"""
Manages authentication and validation tokens for user accounts
"""

from django.contrib.auth.tokens import PasswordResetTokenGenerator

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """
    Token used to verify email and activate a new user account
    """

    def _make_hash_value(self, user, timestamp):
        return f"{user.pk}{timestamp}{user.profile.email_confirmed}"

account_activation_token = AccountActivationTokenGenerator()
