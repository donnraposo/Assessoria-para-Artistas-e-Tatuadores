from rest_framework import serializers


class PortfolioUploadRequestSerializer(serializers.Serializer):
    original_name = serializers.CharField(max_length=255)
    content_type = serializers.ChoiceField(choices=["image/jpeg", "image/png", "image/webp"])
    size_bytes = serializers.IntegerField(min_value=1, max_value=10 * 1024 * 1024)
    caption = serializers.CharField(max_length=300, allow_blank=True, required=False)
    style = serializers.CharField(max_length=80, allow_blank=True, required=False)
    position = serializers.IntegerField(min_value=0, max_value=65535, required=False)
