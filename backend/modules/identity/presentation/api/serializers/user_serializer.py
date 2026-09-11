from rest_framework import serializers

from modules.identity.infrastructure.persistence.models import User


class UserSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "email", "full_name", "roles"]

    def get_roles(self, user: User) -> list[str]:
        return list(user.roles.select_related("role").values_list("role__code", flat=True))
