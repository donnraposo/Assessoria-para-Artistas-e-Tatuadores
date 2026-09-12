from modules.artists.domain.enums import ApplicationStatus
from modules.artists.infrastructure.persistence.models import ArtistProfile
from modules.guests.infrastructure.persistence.models import Guest
from modules.studios.domain.enums import StudioStatus
from modules.studios.infrastructure.persistence.models import Studio


class OperationsReferenceService:
    @staticmethod
    def build() -> dict:
        return {
            "artists": list(
                ArtistProfile.objects.filter(
                    artistapplication__status=ApplicationStatus.APPROVED,
                )
                .values("id", "professional_name", "currency")
                .order_by("professional_name")
            ),
            "studios": list(
                Studio.objects.filter(status=StudioStatus.APPROVED)
                .values("id", "name", "city", "country_code")
                .order_by("name")
            ),
            "guests": list(
                Guest.objects.values(
                    "id",
                    "artist_id",
                    "city",
                    "country_code",
                    "currency",
                    "starts_on",
                    "ends_on",
                    "status",
                ).order_by("-starts_on")
            ),
        }
