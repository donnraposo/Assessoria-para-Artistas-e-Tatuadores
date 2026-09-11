from rest_framework import serializers

from modules.artists.infrastructure.persistence.models import ArtistAvailability


class ArtistAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistAvailability
        exclude = ["artist"]
        read_only_fields = [
            "id",
            "changed_by_advisory",
            "change_reason",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        if attrs["ends_at"] <= attrs["starts_at"]:
            raise serializers.ValidationError("The end time must be after the start time.")
        artist = self.context["artist"]
        overlap = ArtistAvailability.objects.filter(
            artist=artist,
            starts_at__lt=attrs["ends_at"],
            ends_at__gt=attrs["starts_at"],
        )
        if self.instance:
            overlap = overlap.exclude(pk=self.instance.pk)
        if overlap.exists():
            raise serializers.ValidationError(
                "The time range overlaps another availability window."
            )
        return attrs
