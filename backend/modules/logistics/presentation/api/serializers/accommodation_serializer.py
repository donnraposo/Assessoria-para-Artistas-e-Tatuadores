from rest_framework import serializers

from modules.logistics.application.services import AccommodationService
from modules.logistics.infrastructure.persistence.models import Accommodation


class AccommodationSerializer(serializers.ModelSerializer):
    has_private_document = serializers.SerializerMethodField()

    class Meta:
        model = Accommodation
        exclude = ["guest", "created_by"]
        read_only_fields = ["id", "created_at", "updated_at", "has_private_document"]
        extra_kwargs = {"private_document_key": {"write_only": True}}

    def get_has_private_document(self, instance) -> bool:
        return bool(instance.private_document_key)

    def create(self, validated_data):
        return AccommodationService.create(
            guest=self.context["guest"],
            actor=self.context["request"].user,
            **validated_data,
        )

    def update(self, instance, validated_data):
        return AccommodationService.update(
            accommodation=instance,
            actor=self.context["request"].user,
            **validated_data,
        )
