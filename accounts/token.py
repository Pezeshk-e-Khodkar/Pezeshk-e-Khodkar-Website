from django.contrib.auth.tokens import PasswordResetTokenGenerator


# Activation token generator
class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.is_active) + str(user.pk) + str(timestamp)
        )


# Generate token
token_generator = AccountActivationTokenGenerator()
