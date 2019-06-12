from rest_framework import serializers
from .models import Venues
class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venues
        fields = '__all__'