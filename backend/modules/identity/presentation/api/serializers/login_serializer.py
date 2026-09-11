from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate(self, attrs):
        request = self.context.get("request")
        user = authenticate(
            request=request,
            email=attrs["email"].lower(),
            password=attrs["password"],
        )
        if user is None or not user.is_active:
            raise AuthenticationFailed("Invalid credentials.")
        attrs["user"] = user
        return attrs
