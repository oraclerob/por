#-----------------------------------------------------------------------------
# Copyright (c) 2019, Rob Mascaro
#
# Distributed under the terms of the GNU General Public License (version 3or later)
#
# The full license is in the file LICENSE, distributed with this software.
#
#-----------------------------------------------------------------------------

"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "por.settings")

application = get_wsgi_application()



