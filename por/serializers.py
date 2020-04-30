#-----------------------------------------------------------------------------
# Copyright (c) 2019, Rob Mascaro
#
# Distributed under the terms of the GNU General Public License (version 3or later)
#
# The full license is in the file LICENSE, distributed with this software.
#
#-----------------------------------------------------------------------------

from rest_framework import serializers
from .models import Venues
class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venues
        fields = '__all__'