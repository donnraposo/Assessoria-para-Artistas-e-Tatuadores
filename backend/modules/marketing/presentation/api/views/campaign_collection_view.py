from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.identity.presentation.api.permissions import HasAdvisoryRole
from modules.marketing.infrastructure.persistence.models import Campaign
from modules.marketing.presentation.api.serializers import CampaignSerializer


class CampaignCollectionView(APIView):
    permission_classes = [HasAdvisoryRole]

    def get(self, request: Request) -> Response:
        campaigns = Campaign.objects.select_related("guest")
        guest_id = request.query_params.get("guest")
        if guest_id:
            campaigns = campaigns.filter(guest_id=guest_id)
        return Response(CampaignSerializer(campaigns, many=True).data)

    def post(self, request: Request) -> Response:
        serializer = CampaignSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
        except ValueError as error:
            return Response({"detail": str(error)}, status=status.HTTP_409_CONFLICT)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
