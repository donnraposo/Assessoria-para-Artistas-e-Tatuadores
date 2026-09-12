from decimal import Decimal


class ArtistCommercialFloor:
    """RN-016 and RN-017: the value declared by the Artist is the negotiation floor."""

    @staticmethod
    def ensure_respected(artist_minimum: Decimal, proposal_minimum: Decimal) -> None:
        if proposal_minimum < artist_minimum:
            raise ValueError(
                "The proposal minimum cannot be below the minimum declared by the Artist."
            )
