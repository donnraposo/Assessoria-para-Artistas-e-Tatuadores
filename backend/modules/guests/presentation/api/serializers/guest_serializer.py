from rest_framework import serializers

from modules.guests.infrastructure.persistence.models import Guest


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = "__all__"
