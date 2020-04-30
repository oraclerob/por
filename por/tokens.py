#-----------------------------------------------------------------------------
# Copyright (c) 2019, Rob Mascaro
#
# Distributed under the terms of the GNU General Public License (version 3or later)
#
# The full license is in the file LICENSE, distributed with this software.
#
#-----------------------------------------------------------------------------

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.profile.email_confirmed)
        )

account_activation_token = AccountActivationTokenGenerator()