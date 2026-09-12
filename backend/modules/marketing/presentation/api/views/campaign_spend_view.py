from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.identity.presentation.api.permissions import HasAdvisoryRole
from modules.marketing.infrastructure.persistence.models import Campaign
from modules.marketing.presentation.api.serializers import AdSpendSerializer


class CampaignSpendView(APIView):
    permission_classes = [HasAdvisoryRole]

    def post(self, request: Request, campaign_id) -> Response:
        campaign = Campaign.objects.get(pk=campaign_id)
        serializer = AdSpendSerializer(
            data=request.data,
            context={"request": request, "campaign": campaign},
        )
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
        except ValueError as error:
            return Response({"detail": str(error)}, status=status.HTTP_409_CONFLICT)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
