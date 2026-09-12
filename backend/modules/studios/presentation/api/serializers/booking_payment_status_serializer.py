from rest_framework import serializers


class BookingPaymentStatusSerializer(serializers.Serializer):
    payment_status = serializers.ChoiceField(choices=[("PENDING", "Pending"), ("PAID", "Paid")])
