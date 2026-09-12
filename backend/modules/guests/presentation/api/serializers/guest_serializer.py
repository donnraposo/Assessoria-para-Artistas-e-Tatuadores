from rest_framework import serializers

from modules.guests.infrastructure.persistence.models import Guest


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = [
            "id",
            "proposal",
            "artist",
            "city",
            "country_code",
            "starts_on",
            "ends_on",
            "timezone",
            "currency",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields
