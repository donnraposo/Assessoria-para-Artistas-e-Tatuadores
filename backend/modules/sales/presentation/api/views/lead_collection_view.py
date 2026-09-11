from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.identity.presentation.api.permissions import HasAdvisoryRole
from modules.sales.infrastructure.persistence.models import Lead
from modules.sales.presentation.api.serializers import LeadSerializer


class LeadCollectionView(APIView):
    permission_classes = [HasAdvisoryRole]

    def get(self, request: Request) -> Response:
        leads = Lead.objects.select_related("guest")
        guest_id = request.query_params.get("guest")
        if guest_id:
            leads = leads.filter(guest_id=guest_id)
        return Response(LeadSerializer(leads, many=True).data)

    def post(self, request: Request) -> Response:
        serializer = LeadSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
